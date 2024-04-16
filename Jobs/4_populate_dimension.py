import pandas as pd
import os
from sqlalchemy import create_engine, text

DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'pipeline_dados'
DB_PORT = 5432
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

current_dir = os.path.dirname(os.path.realpath(__file__))
pipeline_dir = os.path.join(current_dir, "..")
data_dir = os.path.join(pipeline_dir, "Data")

engine = create_engine(DATABASE_URL)

# Load data
full_df = pd.read_csv(os.path.join(data_dir, 'traditional.csv'))

# Process each dimension separately and handle dependencies
# Update 'game_dimension'
game_cols = ['gameid', 'date', 'type', 'season']
game_df = full_df[game_cols]
game_df.rename(columns={'date': 'game_date', 'type': 'game_type'}, inplace=True)  # Rename the column to match the database schema

# Instead of dropping and recreating the table, update or append
with engine.connect() as conn:
    game_df.to_sql('game_dimension', conn, if_exists='append', index=False)  # Consider handling updates manually if necessary

# Similarly handle other tables
team_cols = ['teamid', 'team', 'home', 'away']
team_df = full_df[team_cols]
team_df.to_sql('team_dimension', engine, if_exists='append', index=False)  # Same handling as game_dimension

performance_cols = ['gameid', 'playerid', 'teamid', 'Min_played', 'PTS', 'FGM', 'FGA']
performance_df = full_df[performance_cols]
performance_df.to_sql('performance_dimension', engine, if_exists='append', index=False)

outcome_cols = ['gameid', 'win', 'plus_minus', 'teamid']
outcome_df = full_df[outcome_cols]
outcome_df.to_sql('outcome_dimension', engine, if_exists='append', index=False)

engine.dispose()
