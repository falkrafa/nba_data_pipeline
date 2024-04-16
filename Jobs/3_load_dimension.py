import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine

DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'pipeline_dados'
DB_PORT = 5432

current_dir = os.path.dirname(os.path.realpath(__file__))
pipeline_dir = os.path.join(current_dir, "..")
table_dir = os.path.join(pipeline_dir, "Tables")

conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
cursor = conn.cursor()

with open(os.path.join(table_dir, 'T1.sql'), 'r') as file:
    cursor.execute(file.read())

sql_files = ['T2.sql', 'T3.sql', 'T4.sql']
for file_name in sql_files:
    with open(os.path.join(table_dir, file_name), 'r') as file:
        cursor.execute(file.read())

conn.commit()
conn.close()
