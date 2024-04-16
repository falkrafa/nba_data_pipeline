import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine
# from ..config.constants import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'pipeline_dados'
DB_PORT = 5432

current_dir = os.path.dirname(os.path.realpath(__file__))
pipeline_dir = os.path.join(current_dir, "..")
data_dir = os.path.join(pipeline_dir, "Data")

conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
df = pd.read_csv(f'{data_dir}/traditional.csv')
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

df.to_sql('nba_data', engine, if_exists='replace', index=False)

conn.close()
