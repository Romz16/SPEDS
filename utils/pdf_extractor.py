from PyPDF2 import PdfReader


def extrair_texto_pdf(caminho_pdf):
    reader = PdfReader(caminho_pdf)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto
