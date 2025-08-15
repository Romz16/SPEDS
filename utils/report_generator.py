import os

def gerar_relatorio_markdown(sped_nome: str, parecer, saida_path: str):
    os.makedirs(os.path.dirname(saida_path), exist_ok=True)

    with open(saida_path, "w", encoding="utf-8") as f:
        # Convertendo para string (se for RunResponse)
        texto = parecer.content if hasattr(parecer, "content") else str(parecer)
        f.write(f"# Análise do SPED: {sped_nome}\n\n")
        f.write(texto)
