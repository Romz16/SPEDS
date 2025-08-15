# main.py
import json
import sped_parser
import pre_validator
import llm_interpreter


def main():
    """
    Função principal que orquestra o fluxo completo da análise de SPEDs.
    """
    print("--- INÍCIO DA ANÁLISE COMPARATIVA DE SPEDs FISCAIS ---")

    # Defina os caminhos para seus arquivos SPED.
    # Certifique-se que estes arquivos estão na mesma pasta do script.
    sped_mes1_path = "sped_mes_2.txt"
    sped_mes2_path = "sped_mes_1.txt"

    # --- ETAPA 1: PARSING DOS ARQUIVOS ---
    dados_sped1 = sped_parser.parse_sped_file(sped_mes1_path)
    dados_sped2 = sped_parser.parse_sped_file(sped_mes2_path)

    if not dados_sped1 or not dados_sped2:
        print(
            "\nProcesso interrompido devido a erro no parsing de um ou ambos os arquivos."
        )
        return

    # --- ETAPA 2: PRÉ-PROCESSAMENTO E VALIDAÇÃO ---
    print("\nIniciando validações programáticas e análise comparativa...")
    achados_da_analise = pre_validator.analisar_comparativamente(
        dados_sped1, dados_sped2
    )
    print(
        f"Análise de regras concluída. Foram encontrados {len(achados_da_analise)} pontos de atenção."
    )

    # Salva o resultado técnico intermediário em um arquivo JSON
    output_json_path = "resumo_tecnico_analise.json"
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(achados_da_analise, f, indent=4, ensure_ascii=False)
    print(f"Resumo técnico salvo em: {output_json_path}")

    # --- ETAPA 3: INTERPRETAÇÃO COM LLM ---
    relatorio_texto = llm_interpreter.gerar_interpretacao_llm(achados_da_analise)

    # --- ETAPA 4: SALVAR RELATÓRIO FINAL ---
    output_report_path = "relatorio_final.txt"
    with open(output_report_path, "w", encoding="utf-8") as f:
        f.write(relatorio_texto)

    print(
        f"\nRelatório final com a interpretação do especialista salvo em: {output_report_path}"
    )
    print("\n--- PROCESSO CONCLUÍDO COM SUCESSO ---")


if __name__ == "__main__":
    main()
