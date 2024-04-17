CREATE TABLE IF NOT EXISTS performance_fact (
    id SERIAL PRIMARY KEY,
    game_id INT,
    player_id INT,
    minutes_played INT,
    points_scored INT,
    field_goals_made INT,
    field_goals_attempted INT,
    FOREIGN KEY (game_id) REFERENCES game_dimension(id),
    FOREIGN KEY (player_id) REFERENCES performance_dimension(id)
);
