CREATE TABLE IF NOT EXISTS outcome_dimension (
    id SERIAL PRIMARY KEY,
    game_id INT,  -- Use game_id here for foreign key reference
    win BOOLEAN,
    plus_minus INTEGER,  
    FOREIGN KEY (game_id) REFERENCES game_dimension(id)  -- Reference the primary key of game_dimension
);