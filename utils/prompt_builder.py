def construir_prompt(sped_text):
    return (
        "Você é um analista fiscal. Com base nos documentos técnicos e no passo a passo de validação do SPED ICMS/IPI, "
        "avalie o conteúdo a seguir e gere um parecer técnico. Aponte incoerências estruturais, fiscais e valores "
        "anômalos. Caso esteja tudo certo, declare conformidade.\n\n"
        f"SPED analisado:\n\n{sped_text}"
    )
