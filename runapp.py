import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


# Carregar as variáveis do arquivo .env
load_dotenv()

# Configurações do banco de dados a partir das variáveis de ambiente
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')
schema = os.getenv('DB_SCHEMA')
table_name = os.getenv('DB_TABLE')

# Criação da string de conexão
connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
engine = create_engine(connection_string)

# Carregar dados do CSV para um DataFrame
csv_file = './mundo_transfermarkt_competicoes_brasileirao_serie_a.csv'
df = pd.read_csv(csv_file)

# Carregar o DataFrame para a tabela MySQL, especificando o schema
df.to_sql(table_name, con=engine, if_exists='replace', index=False, schema=schema)

print("Dados carregados com sucesso!")
