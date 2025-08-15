# sped_parser.py
import pandas as pd
from typing import Dict
import logging

# Configuração básica de logging para feedback durante a execução
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_sped_file(filepath: str) -> Dict[str, pd.DataFrame]:
    """
    Lê um arquivo SPED do caminho especificado e o converte em um dicionário
    de DataFrames do Pandas, onde cada chave é um tipo de registro (ex: 'C100').
    """
    logging.info(f"Iniciando o parsing do arquivo: {filepath}")
    records = {}
    try:
        # Abre o arquivo com encoding 'latin-1', comum em sistemas legados brasileiros.
        with open(filepath, "r", encoding="latin-1") as f:
            for line in f:
                # Remove espaços em branco e quebras de linha, depois divide pelo pipe '|'
                fields = line.strip().split("|")
                # Linhas válidas de SPED têm conteúdo entre os pipes
                if len(fields) > 2:
                    record_type = fields[1]
                    if record_type not in records:
                        records[record_type] = []
                    # Adiciona a lista de campos (sem os pipes das pontas)
                    records[record_type].append(fields[1:-1])

    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {filepath}")
        return {}
    except Exception as e:
        logging.error(f"Erro inesperado ao ler o arquivo {filepath}: {e}")
        return {}

    dataframes = {}
    for record_type, data_list in records.items():
        try:
            # Cria colunas genéricas. Para uma análise mais profunda,
            # seria necessário mapear cada registro para suas colunas nomeadas
            # conforme o Guia Prático da EFD.
            num_cols = len(data_list[0])
            columns = [f"CAMPO_{i+1}" for i in range(num_cols)]
            df = pd.DataFrame(data_list, columns=columns)
            # Renomeia a primeira coluna para 'REG' para facilitar a identificação
            df.rename(columns={"CAMPO_1": "REG"}, inplace=True)
            dataframes[record_type] = df
        except Exception as e:
            logging.warning(
                f"Não foi possível criar DataFrame para o registro {record_type}: {e}"
            )

    logging.info(
        f"Parsing de {filepath} concluído. {len(dataframes)} tipos de registros foram carregados."
    )
    return dataframes
