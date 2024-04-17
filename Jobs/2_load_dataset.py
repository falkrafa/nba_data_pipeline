import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine

# Defina as suas variáveis de conexão com o banco de dados
DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'pipeline_dados'
DB_PORT = 5432

# Localização dos arquivos
current_dir = os.path.dirname(os.path.realpath(__file__))
pipeline_dir = os.path.join(current_dir, "..")
data_dir = os.path.join(pipeline_dir, "Data")

conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)

# Leitura do CSV
df = pd.read_csv(f'{data_dir}/traditional.csv')

# Selecionar 10% dos dados aleatoriamente
df_sampled = df.sample(frac=0.1, random_state=42)

df_sampled[['ano', 'mes', 'dia']] = df_sampled['date'].str.split('-', expand=True)
df.rename(columns={'+/-': 'plus_minus'}, inplace=True)
df.rename(columns={'MIN': 'min_played'}, inplace=True)

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

df_sampled.to_sql('nba_data', engine, if_exists='replace', index=False)

conn.close()
