# main.py
import json
import sped_parser
import pre_validator
import llm_interpreter
from typing import Dict
def carregar_configuracao(caminho_arquivo: str) -> Dict:
    """Carrega as configurações do arquivo JSON."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"AVISO: Arquivo de configuração '{caminho_arquivo}' não encontrado. Usando regras padrão.")
        return {
            "limiares": {},
            "regras_ativas": {key: True for key in ["validar_fluxo_estoque", "validar_apuracao_icms", "validar_sequencia_notas"]}
        }

def main():
    print("--- INÍCIO DA ANÁLISE COMPARATIVA DE SPEDs FISCAIS (v2.0) ---")
    
    # Carrega as configurações
    config = carregar_configuracao('config.json')

    sped_anterior_path = 'sped_mes_1.txt' # Ex: Junho
    sped_atual_path = 'sped_mes_2.txt'       # Ex: Julho

    # --- ETAPA 1: PARSING DOS ARQUIVOS ---
    dados_sped_anterior = sped_parser.parse_sped_file(sped_anterior_path)
    dados_sped_atual = sped_parser.parse_sped_file(sped_atual_path)

    if not dados_sped_anterior or not dados_sped_atual:
        print("\nProcesso interrompido devido a erro no parsing.")
        return

    # --- ETAPA 2: PRÉ-PROCESSAMENTO E VALIDAÇÃO ---
    print("\nIniciando validações programáticas avançadas...")
    achados = pre_validator.analisar_comparativamente(dados_sped_anterior, dados_sped_atual, config)
    print(f"Análise de regras concluída. Foram encontrados {len(achados)} pontos de atenção.")

    output_json_path = 'resumo_tecnico_analise.json'
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(achados, f, indent=4, ensure_ascii=False)
    print(f"Resumo técnico salvo em: {output_json_path}")

    relatorio_texto = llm_interpreter.gerar_interpretacao_llm(achados)

    output_report_path = 'relatorio_final.txt'
    with open(output_report_path, 'w', encoding='utf-8') as f:
        f.write(relatorio_texto)
    print(f"\nRelatório final com a interpretação do especialista salvo em: {output_report_path}")
    print("\n--- PROCESSO CONCLUÍDO COM SUCESSO ---")

if __name__ == '__main__':
    main()