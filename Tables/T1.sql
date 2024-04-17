CREATE TABLE IF NOT EXISTS game_dimension (
    id SERIAL PRIMARY KEY,
    gameid VARCHAR(255),
    game_date VARCHAR(50),
    game_type VARCHAR(50),
    season VARCHAR(20)
);