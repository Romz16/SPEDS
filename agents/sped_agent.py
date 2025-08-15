import os
from agno.agent import Agent
from agno.document.base import Document
from agno.knowledge.document import DocumentKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.models.ollama import Ollama
from utils.preprocessor import preprocess_sped
from utils.prompt_builder import construir_prompt
from utils.report_generator import gerar_relatorio_markdown
from agno.embedder.ollama import OllamaEmbedder
from utils.pdf_extractor import extrair_texto_pdf


def construir_agente():
    # Extrai texto dos PDFs
    guia_tecnico_texto = extrair_texto_pdf("docs/guia_tecnico.pdf")
    passo_a_passo_texto = extrair_texto_pdf("docs/passo_a_passo.pdf")

    # Cria documentos para base de conhecimento
    documents = [
        Document(content=guia_tecnico_texto, meta_data={"source": "guia_tecnico"}),
        Document(content=passo_a_passo_texto, meta_data={"source": "passo_a_passo"}),
    ]

    # Embedder local via Ollama com mxbai
    embedder = OllamaEmbedder(
        id="mxbai-embed-large:latest",
        dimensions=1024,  # Esse é o tamanho padrão dos embeddings desse modelo
    )
    # Configura o banco vetorial
    vector_db = LanceDb(
        table_name="sped_docs", uri="knowledge/lancedb", embedder=embedder
    )

    knowledge_base = DocumentKnowledgeBase(documents=documents, vector_db=vector_db)
    knowledge_base.load(recreate=False)

    agent = Agent(
        session_id="session_sped",
        user_id="analista_sped",
        model=Ollama(id="llama3.1:latest"),
        knowledge=knowledge_base,
        search_knowledge=True,
        show_tool_calls=True,
        markdown=True,
    )
    return agent


def analisar_speds(lista_caminhos):
    agente = construir_agente()
    for caminho in lista_caminhos:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        sped_formatado = preprocess_sped(conteudo)
        prompt = construir_prompt(sped_formatado)

        print(f"\n📁 Analisando: {os.path.basename(caminho)}\n")
        resposta = agente.run(prompt)
        print(resposta)

        gerar_relatorio_markdown(
            sped_nome=os.path.basename(caminho),
            parecer=resposta,
            saida_path=f"relatorios/{os.path.basename(caminho).replace('.txt', '.md')}",
        )
