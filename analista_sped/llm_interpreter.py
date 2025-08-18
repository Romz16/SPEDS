# llm_interpreter.py
import json
import ollama
from typing import List, Dict, Any


def gerar_interpretacao_llm(achados: List[Dict[str, Any]]) -> str:
    if not achados:
        return "Análise concluída. Nenhuma inconsistência foi encontrada pelo script de pré-processamento."

    achados_json_str = json.dumps(achados, indent=2, ensure_ascii=False)

    prompt = f"""
    Você é um Auditor Fiscal Sênior, especialista em SPED Fiscal e legislação tributária.
    Sua tarefa é analisar um resumo de inconsistências, gerado por um script, que comparou dois arquivos SPED de meses consecutivos.
    Para cada item listado no JSON abaixo, forneça uma análise detalhada e profissional.

    Seu relatório final deve ser bem estruturado e conter, para cada inconsistência:
    1.  **Gravidade do Risco:** Classifique o risco como Baixo, Médio ou Alto.
    2.  **Explicação Detalhada:** Descreva o que a inconsistência significa em termos práticos e por que é um problema fiscal.
    3.  **Possíveis Causas:** Liste as causas mais comuns para este tipo de erro (ex: erro de digitação, falha de processo, omissão intencional).
    4.  **Ações Recomendadas:** Forneça um passo a passo claro que o analista deve seguir para investigar e corrigir o problema.

    Analise os seguintes dados:
    {achados_json_str}

    Gere a resposta em formato de relatório, organizando a análise para cada ponto encontrado. Use markdown para formatar o texto.
    """

    print("\nEnviando dados para análise do Llama 3. Isso pode levar um momento...")

    try:
        response = ollama.generate(
            model="llama3.1:latest", 
            prompt=prompt,
        )

        # Extrai o texto da resposta do dicionário retornado
        print("Relatório de interpretação recebido do LLM.")
        return response.get(
            "response", "Nenhuma resposta textual foi recebida do modelo."
        )

    except ollama.ResponseError as e:
        error_message = f"Erro retornado pela API do Ollama: {e.error}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = (
            f"Ocorreu um erro inesperado ao se comunicar com o Ollama: {e}\n"
            "DICAS:\n"
            "1. Verifique se o serviço do Ollama está em execução no seu computador.\n"
            "2. Confirme se o modelo 'llama3.1:latest' foi baixado com o comando 'ollama pull llama3.1:latest'."
        )
        print(error_message)
        return error_message
