# pre_validator.py
from typing import Dict, List, Any
import pandas as pd

def analisar_comparativamente(sped_anterior: Dict[str, pd.DataFrame], sped_atual: Dict[str, pd.DataFrame], config: Dict) -> List[Dict[str, Any]]:
    achados = []
    regras = config.get("regras_ativas", {})
    limiares = config.get("limiares", {})

    # REGRA 1: Validação do Fluxo de Estoque
    if regras.get("validar_fluxo_estoque") and 'H005' in sped_anterior and 'H005' in sped_atual and 'C170' in sped_atual:
        try:
            h005_anterior = sped_anterior['H005']
            estoque_inicial = pd.to_numeric(h005_anterior.loc[h005_anterior['MOT_INV'] == '01', 'VL_INV'], errors='coerce').sum()
            c170_atual = sped_atual['C170']
            total_entradas = pd.to_numeric(c170_atual['VL_ITEM'], errors='coerce').sum()
            h005_atual = sped_atual['H005']
            estoque_final_declarado = pd.to_numeric(h005_atual.loc[h005_atual['MOT_INV'] == '01', 'VL_INV'], errors='coerce').sum()
            estoque_final_esperado = estoque_inicial + total_entradas
            if abs(estoque_final_esperado - estoque_final_declarado) > 0.01:
                achados.append({
                    "bloco": "H e C", "registro": "H005/C170", "tipo_inconsistencia": "Fluxo de Estoque Inconsistente",
                    "descricao": f"Estoque inicial (R${estoque_inicial:.2f}) + Entradas (R${total_entradas:.2f}) = Esperado (R${estoque_final_esperado:.2f}). O declarado foi R${estoque_final_declarado:.2f}.",
                    "irregularidade_possivel": "Omissão de vendas ou erro no registro de inventário."
                })
        except KeyError as e:
             achados.append({"bloco": "H ou C", "tipo_inconsistencia": "Alerta de Estrutura", "descricao": f"Não foi possível validar o estoque. Coluna esperada {e} não encontrada."})

    # REGRA 2: Validação da Apuração de ICMS
    if regras.get("validar_apuracao_icms") and 'E110' in sped_atual and 'C170' in sped_atual:
        icms_apurado_itens = pd.to_numeric(sped_atual['C170']['VL_ICMS'], errors='coerce').sum()
        icms_declarado_debitos = pd.to_numeric(sped_atual['E110']['VL_TOT_DEBITOS'], errors='coerce').sum()
        if icms_apurado_itens > 0 and icms_declarado_debitos == 0:
            achados.append({
                "bloco": "E e C", "registro": "E110/C170", "tipo_inconsistencia": "Apuração de ICMS Incompatível",
                "descricao": f"A soma do ICMS nos itens (Bloco C) foi de R${icms_apurado_itens:.2f}, mas o total de débitos no Bloco E foi R${icms_declarado_debitos:.2f}.",
                "irregularidade_possivel": "Débito de imposto omitido."
            })

    # REGRA 3: Validação da Sequência Numérica de Notas
    if regras.get("validar_sequencia_notas") and 'C100' in sped_anterior and 'C100' in sped_atual:
        max_num_nota_anterior = pd.to_numeric(sped_anterior['C100']['NUM_DOC'], errors='coerce').max()
        min_num_nota_atual = pd.to_numeric(sped_atual['C100']['NUM_DOC'], errors='coerce').min()
        if min_num_nota_atual < max_num_nota_anterior:
            achados.append({
                "bloco": "C", "registro": "C100", "tipo_inconsistencia": "Quebra na Sequência Numérica de Notas",
                "descricao": f"Numeração de notas regrediu. Máximo anterior: {max_num_nota_anterior:.0f}, Mínimo atual: {min_num_nota_atual:.0f}.",
                "irregularidade_possivel": "Omissão de notas fiscais."
            })
            
    # REGRA 4: Análise de Notas Canceladas
    if regras.get("validar_notas_canceladas") and 'C100' in sped_anterior and 'C100' in sped_atual:
        total_notas_ant = len(sped_anterior['C100'])
        canceladas_ant = len(sped_anterior['C100'][sped_anterior['C100']['COD_SIT'] == '02'])
        perc_canceladas_ant = (canceladas_ant / total_notas_ant * 100) if total_notas_ant > 0 else 0

        total_notas_atual = len(sped_atual['C100'])
        canceladas_atual = len(sped_atual['C100'][sped_atual['C100']['COD_SIT'] == '02'])
        perc_canceladas_atual = (canceladas_atual / total_notas_atual * 100) if total_notas_atual > 0 else 0

        if perc_canceladas_atual > (perc_canceladas_ant + limiares.get("variacao_maxima_notas_percentual", 50.0)):
             achados.append({
                "bloco": "C", "registro": "C100", "tipo_inconsistencia": "Aumento Suspeito de Notas Canceladas",
                "descricao": f"O percentual de notas canceladas aumentou de {perc_canceladas_ant:.2f}% para {perc_canceladas_atual:.2f}%.",
                "irregularidade_possivel": "Tentativa de anular operações já ocorridas para reduzir imposto."
            })

    # --- NOVA REGRA 5 (CORRIGIDA) ---
    # Lógica foi reescrita para ser mais simples e correta.
    if regras.get("validar_cfop_vs_operacao") and 'C100' in sped_atual and 'C170' in sped_atual:
        # Pega o tipo de operação do primeiro registro C100 (0=Entrada, 1=Saída)
        # Nossos exemplos só têm um C100, então isso funciona.
        tipo_operacao = sped_atual['C100']['IND_OPER'].iloc[0]

        if tipo_operacao == '1': # Se a operação for de SAÍDA
            df_itens = sped_atual['C170']
            # Procura por CFOPs de ENTRADA (começam com 1, 2 ou 3) nos itens
            cfops_de_entrada_em_saida = df_itens[df_itens['CFOP'].str.startswith(('1', '2', '3'))]
            if not cfops_de_entrada_em_saida.empty:
                achados.append({
                    "bloco": "C", "registro": "C170", "tipo_inconsistencia": "CFOP Incompatível com a Operação",
                    "descricao": f"Encontradas {len(cfops_de_entrada_em_saida)} operações de SAÍDA com CFOP de ENTRADA. Exemplo: CFOP {cfops_de_entrada_em_saida['CFOP'].iloc[0]}.",
                    "irregularidade_possivel": "Erro grave de classificação fiscal, afetando toda a apuração."
                })
            
    # REGRA 6: Crédito Indevido sobre Uso e Consumo
    if regras.get("validar_credito_indevido_consumo") and 'C170' in sped_atual:
        cfops_consumo = ['1556', '2556', '3556']
        df_credito_consumo = sped_atual['C170'][
            (sped_atual['C170']['CFOP'].isin(cfops_consumo)) &
            (pd.to_numeric(sped_atual['C170']['VL_ICMS'], errors='coerce') > 0)
        ]
        if not df_credito_consumo.empty:
            achados.append({
                "bloco": "C", "registro": "C170", "tipo_inconsistencia": "Crédito de ICMS Indevido sobre Consumo",
                "descricao": f"Detectado crédito de ICMS em {len(df_credito_consumo)} itens classificados como uso/consumo.",
                "irregularidade_possivel": "Apropriação ilegal de crédito de ICMS, resultando em menor recolhimento."
            })

    return achados