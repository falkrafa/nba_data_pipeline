CREATE TABLE IF NOT EXISTS outcome_dimension (
    gameid VARCHAR(255) PRIMARY KEY,
    win BOOLEAN,
    plus_minus INTEGER,
    teamid VARCHAR(255),
    FOREIGN KEY (gameid) REFERENCES game_dimension(gameid),
    FOREIGN KEY (teamid) REFERENCES team_dimension(teamid)
)