from agno.tools import tool
import re

@tool(name="extrair_cfops", description="Extrai todos os CFOPs do SPED e retorna uma lista distinta")
def extrair_cfops(sped_text: str):
    cfops = set(re.findall(r'\|5\d{3}\|', sped_text))
    return list(cfops)

@tool(name="verificar_blocos_obrigatorios", description="Verifica a presença dos blocos essenciais no SPED")
def verificar_blocos_obrigatorios(sped_text: str):
    blocos = ["0000", "C100", "C170", "H005", "H010", "0500"]
    faltando = [bloco for bloco in blocos if bloco not in sped_text]
    if faltando:
        return f"Blocos ausentes: {', '.join(faltando)}"
    return "Todos os blocos obrigatórios estão presentes."
