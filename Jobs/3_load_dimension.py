import psycopg2
import os

# Database connection details
DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'pipeline_dados'
DB_PORT = 5432

# Function to connect to the PostgreSQL database
def get_connection():
    try:
        conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME, port=DB_PORT)
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Database connection failed: {e}")
        return None

# Function to create tables in the PostgreSQL database
def create_tables(conn):
    if conn is not None:
        cursor = conn.cursor()
        try:
            # Iterate over all files in the Tables directory
            for filename in os.listdir("Tables"):
                if filename.endswith(".sql"):
                    filepath = os.path.join("Tables", filename)
                    with open(filepath, "r") as file:
                        table_definition = file.read()
                        cursor.execute(table_definition)
            conn.commit()
            print("Tables created successfully.")
        except psycopg2.DatabaseError as e:
            conn.rollback()
            print(f"Failed to create tables: {e}")
        finally:
            cursor.close()

# Example function to insert data into the tables with batch transactions
def insert_data(conn, data, column_names, batch_size=100000):
    if conn is not None:
        cursor = conn.cursor()
        
        # Pre-load existing game IDs and team names
        cursor.execute("""SELECT gameid, id FROM game_dimension""")
        values = cursor.fetchall()
        existing_game_ids = {row[0]: row[1] for row in values} # 700K
        
        cursor.execute("SELECT team, id FROM team_dimension")
        existing_team_ids = {row[0]: row[1] for row in values} # 700K
            
        # SQL Insert Statements
        insert_game_query = """
            INSERT INTO game_dimension (gameid, game_date, game_type, season)
            VALUES (%s, %s, %s, %s) RETURNING id
        """
        insert_performance_query = """
            INSERT INTO performance_dimension (player, game_id, playerid, min_played, PTS, FGM, FGA)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        insert_team_query = """
            INSERT INTO team_dimension (team, home, away, game_id, player_id)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id
        """
        insert_outcome_query = """
            INSERT INTO outcome_dimension (game_id, win, plus_minus)
            VALUES (%s, %s, %s)
        """

        insert_performance_fact_query = """
            INSERT INTO performance_fact (game_id, player_id, minutes_played, points_scored, field_goals_made, field_goals_attempted)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        insert_outcome_fact_query = """
            INSERT INTO outcome_fact (game_id, win, plus_minus)
            VALUES (%s, %s, %s)
        """
        
        game_insert_count = 0
        performance_insert_count = 0
        team_insert_count = 0
        outcome_insert_count = 0
        performance_fact_insert_count = 0
        outcome_fact_insert_count = 0

        try:
            for index, row in enumerate(data): # 700 K
                row_values = {column_names[i]: str(row[i]) for i in range(len(column_names))} # 30

                # Game Dimension Insert
                if row_values['gameid'] not in existing_game_ids: # O(n)
                    cursor.execute(insert_game_query, (row_values['gameid'], row_values['date'], row_values['type'], row_values['season']))
                    game_dimension_id = cursor.fetchone()[0]
                    existing_game_ids[row_values['gameid']] = game_dimension_id
                    game_insert_count += 1
                else:
                    game_dimension_id = existing_game_ids[row_values['gameid']]

                # Performance Dimension Insert
                cursor.execute(insert_performance_query, (row_values['player'], game_dimension_id, row_values.get('playerid'), row_values.get('Min_played'), row_values.get('PTS'), row_values.get('FGM'), row_values.get('FGA')))
                performance_dimension_id = cursor.fetchone()[0]  # Obtenha o ID retornado pela operação RETURNING id
                performance_insert_count += 1

                # Team Dimension Insert
                cursor.execute(insert_team_query, (row_values['team'], row_values['home'], row_values['away'], game_dimension_id, performance_dimension_id))
                result = cursor.fetchone()
                if result:
                    team_id = result[0]
                    existing_team_ids[row_values['team']] = team_id
                    team_insert_count += 1

                # Outcome Dimension Insert
                cursor.execute(insert_outcome_query, (game_dimension_id, row_values.get('win', False), row_values.get('+/-')))
                outcome_insert_count += 1

                #fato performance insert

                cursor.execute(insert_performance_fact_query, (game_dimension_id, performance_dimension_id, row_values.get('Min_played'), row_values.get('PTS'), row_values.get('FGM'), row_values.get('FGA')))
                performance_fact_insert_count += 1

                 # Outcome Fact Insert
                cursor.execute(insert_outcome_fact_query, (game_dimension_id, row_values.get('win', False), row_values.get('+/-')))
                outcome_fact_insert_count += 1
                
                # Commit transaction after every batch_size iterations
                if (index + 1) % batch_size == 0:
                    conn.commit()
                    print(f"Processed {index+1} rows; Total games inserted: {game_insert_count}, Total performances inserted: {performance_insert_count}, Total teams inserted: {team_insert_count}, Total outcomes inserted: {outcome_insert_count}")


            # Commit any remaining transactions
            conn.commit()
            print(f"Final data insertion complete. Total games inserted: {game_insert_count}, Total performances inserted: {performance_insert_count}, Total teams inserted: {team_insert_count}, Total outcomes inserted: {outcome_insert_count}")
        except psycopg2.DatabaseError as e:
            conn.rollback()
            print(f"Failed to insert data: {e}")
        finally:
            cursor.close()



def load_data_from_postgres(table_name):
    print(f"Carrying data from table {table_name}...")
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description] if cursor.description else []
            cursor.close()
            return data, column_names
        except psycopg2.Error as e:
            print(f"An error occurred while accessing the database: {e}")
            return [], []  # Return empty lists in case of error
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")
        return [], []  # Return empty lists if connection could not be established


# Main function to manage the database setup
def main():
    conn = get_connection()
    if conn:
        create_tables(conn)
        data, column_names = load_data_from_postgres('nba_data')  # Load data from the appropriate table
        insert_data(conn, data, column_names)
        conn.close()

if __name__ == "__main__":
    main()
