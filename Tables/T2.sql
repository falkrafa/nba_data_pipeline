CREATE TABLE IF NOT EXISTS team_dimension (
    id SERIAL PRIMARY KEY,
    team VARCHAR(255),
    home VARCHAR(255),
    away VARCHAR(255),
    game_id INT,
    FOREIGN KEY (game_id) REFERENCES game_dimension(id)
);
