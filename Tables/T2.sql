CREATE TABLE IF NOT EXISTS performance_dimension (
    id SERIAL PRIMARY KEY,
    player VARCHAR(255),
    game_id INT,  -- Corrected: Use an underscore to match the insertion logic
    playerid VARCHAR(255), 
    Min_played INTEGER,
    PTS INTEGER,
    FGM INTEGER,
    FGA INTEGER,
    FOREIGN KEY (game_id) REFERENCES game_dimension(id)  -- Ensure the foreign key also uses an underscore
);