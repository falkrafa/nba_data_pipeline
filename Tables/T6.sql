CREATE TABLE IF NOT EXISTS outcome_fact (
    id SERIAL PRIMARY KEY,
    game_id INT,
    win BOOLEAN,
    plus_minus INTEGER,
    FOREIGN KEY (game_id) REFERENCES game_dimension(id)
);
