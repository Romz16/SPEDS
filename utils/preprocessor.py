def preprocess_sped(texto):
    # Remove cabeçalhos inúteis e espaços
    linhas = texto.splitlines()
    linhas_limpas = [linha.strip() for linha in linhas if linha.strip() != ""]
    return "\n".join(linhas_limpas)

