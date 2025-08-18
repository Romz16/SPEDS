# sped_parser.py (Versão de Diagnóstico)
import pandas as pd
from typing import Dict
import logging
from schemas import SCHEMAS

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_sped_file(filepath: str) -> Dict[str, pd.DataFrame]:
    logging.info(f"Iniciando o parsing do arquivo: {filepath}")
    records = {}
    try:
        with open(filepath, "r", encoding="latin-1") as f:
            for i, line in enumerate(f):  # Adiciona um contador de linha
                # Ignora linhas vazias
                if not line.strip():
                    continue

                fields = line.strip().split("|")

                # Validação básica da estrutura da linha
                if len(fields) <= 2:
                    logging.warning(
                        f"Linha {i+1} ignorada (formato inválido): {line.strip()}"
                    )
                    continue

                record_type = fields[1]
                if record_type not in records:
                    records[record_type] = []

                # Armazena os campos de dados (tudo entre o primeiro e o último pipe)
                data_fields = fields[1:-1]
                records[record_type].append(data_fields)

    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {filepath}")
        return {}
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {filepath}: {e}")
        return {}

    dataframes = {}
    print("\n--- INÍCIO DO DIAGNÓSTICO DE SCHEMAS ---")  # DEBUG
    for record_type, data_list in records.items():
        try:
            num_cols_data = len(data_list[0])
            columns = [f"CAMPO_{i+1}" for i in range(num_cols_data)]

            if record_type in SCHEMAS:
                schema_cols = SCHEMAS[record_type]

                # --- BLOCO DE DIAGNÓSTICO ---
                # Imprime a comparação para os registros que estão falhando
                if record_type in ["C100", "C170", "D100", "E110"]:
                    print(f"\n[DEBUG] Registro: {record_type}")
                    print(f"  - Campos encontrados no arquivo: {num_cols_data}")
                    print(f"  - Campos esperados no schema.py: {len(schema_cols)}")
                    if len(schema_cols) != num_cols_data:
                        print("  - VEREDITO: NÃO CORRESPONDEM! Usando nomes genéricos.")
                # --- FIM DO BLOCO DE DIAGNÓSTICO ---

                if len(schema_cols) == num_cols_data:
                    columns = schema_cols
                else:
                    logging.warning(
                        f"Schema para registro '{record_type}' não bate com os dados. Usando nomes genéricos."
                    )

            df = pd.DataFrame(data_list, columns=columns)
            dataframes[record_type] = df
        except Exception as e:
            logging.warning(
                f"Não foi possível criar DataFrame para o registro {record_type}: {e}"
            )

    print("\n--- FIM DO DIAGNÓSTICO DE SCHEMAS ---\n")  # DEBUG
    logging.info(
        f"Parsing de {filepath} concluído. {len(dataframes)} tipos de registros foram carregados."
    )
    return dataframes
