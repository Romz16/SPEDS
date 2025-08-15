# pre_validator.py
from typing import Dict, List, Any
import pandas as pd

def analisar_comparativamente(sped_anterior: Dict[str, pd.DataFrame], sped_atual: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
    """
    Orquestra a análise comparativa entre dois SPEDs (mês anterior e mês atual),
    implementando regras de validação fiscal complexas.
    """
    achados = []

    # --- REGRA 1: Validação do Fluxo de Estoque (Bloco H vs Bloco C) ---
    # A regra mais importante: Estoque Final = Estoque Inicial + Entradas - Saídas
    if 'H005' in sped_anterior and 'H005' in sped_atual and 'C170' in sped_atual:
        try:
            # Pega o estoque final do mês anterior, que é o inicial do mês atual
            h005_anterior = sped_anterior['H005']
            estoque_inicial = pd.to_numeric(h005_anterior.loc[h005_anterior['CAMPO_4'] == '1', 'CAMPO_3'], errors='coerce').sum()

            # Soma o valor de todas as entradas de mercadorias no mês atual
            # Assumindo, para este exemplo, que todos C170 são entradas
            c170_atual = sped_atual['C170']
            # CAMPO_7 é o VL_ITEM
            total_entradas = pd.to_numeric(c170_atual['CAMPO_7'], errors='coerce').sum()

            # Pega o estoque final declarado no mês atual
            h005_atual = sped_atual['H005']
            estoque_final_declarado = pd.to_numeric(h005_atual.loc[h005_atual['CAMPO_4'] == '1', 'CAMPO_3'], errors='coerce').sum()

            # Calcula o estoque final esperado (assumindo sem saídas para simplificar)
            estoque_final_esperado = estoque_inicial + total_entradas

            # Compara o valor esperado com o declarado, com uma pequena margem de tolerância
            if abs(estoque_final_esperado - estoque_final_declarado) > 0.01:
                achados.append({
                    "bloco": "H e C", "registro": "H005 / C170", "tipo_inconsistencia": "Inconsistência Crítica no Fluxo de Estoque",
                    "descricao": f"O estoque não bate. Incial: R${estoque_inicial:.2f} + Entradas: R${total_entradas:.2f} = Esperado: R${estoque_final_esperado:.2f}. Declarado foi R${estoque_final_declarado:.2f}.",
                    "irregularidade_possivel": "Omissão de vendas (vendas não registradas) ou erro grave no registro de entradas/inventário."
                })
        except KeyError as e:
            # Adiciona um alerta se alguma coluna esperada não for encontrada
            achados.append({
                "bloco": "H ou C", "registro": "-", "tipo_inconsistencia": "Alerta de Estrutura",
                "descricao": f"Não foi possível validar o fluxo de estoque pois a coluna {e} não foi encontrada em um dos arquivos.",
                "irregularidade_possivel": "Arquivo SPED com estrutura incompleta."
            })


    # --- REGRA 2: Validação da Apuração de ICMS (Bloco E vs Bloco C) ---
    if 'E110' in sped_atual and 'C170' in sped_atual:
        # CAMPO_15 no C170 é o VL_ICMS
        icms_apurado_itens = pd.to_numeric(sped_atual['C170']['CAMPO_15'], errors='coerce').sum()
        # CAMPO_3 no E110 é o VL_TOT_DEBITOS
        icms_declarado_debitos = pd.to_numeric(sped_atual['E110']['CAMPO_3'], errors='coerce').sum()
        
        if icms_apurado_itens > 0 and icms_declarado_debitos == 0:
            achados.append({
                "bloco": "E e C", "registro": "E110 / C170", "tipo_inconsistencia": "Apuração de ICMS Incompatível",
                "descricao": f"A soma do ICMS nos itens (Bloco C) é de R${icms_apurado_itens:.2f}, mas o total de débitos no Bloco E é R${icms_declarado_debitos:.2f}.",
                "irregularidade_possivel": "Débito de imposto omitido, levando ao não recolhimento do ICMS devido."
            })

    # --- REGRA 3: Validação da Sequência Numérica de Notas (Bloco C) ---
    if 'C100' in sped_anterior and 'C100' in sped_atual:
        # CAMPO_9 no C100 é o NUM_DOC
        max_num_nota_anterior = pd.to_numeric(sped_anterior['C100']['CAMPO_9'], errors='coerce').max()
        min_num_nota_atual = pd.to_numeric(sped_atual['C100']['CAMPO_9'], errors='coerce').min()

        if min_num_nota_atual < max_num_nota_anterior:
            achados.append({
                "bloco": "C", "registro": "C100", "tipo_inconsistencia": "Quebra na Sequência Numérica de Notas",
                "descricao": f"A numeração de notas regrediu. O número máximo no mês anterior foi {max_num_nota_anterior:.0f} e o mínimo no mês atual foi {min_num_nota_atual:.0f}.",
                "irregularidade_possivel": "Pode indicar omissão de notas fiscais (a 'lacuna' entre os números não foi declarada) ou reinício indevido de série."
            })
    
    return achados