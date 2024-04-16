CREATE TABLE IF NOT EXISTS performance_dimension (
    player VARCHAR(255)
    gameid VARCHAR(255),
    playerid VARCHAR(255),
    teamid VARCHAR(255),
    Min_played INTEGER,
    PTS INTEGER,
    FGM INTEGER,
    FGA INTEGER,
    PRIMARY KEY (gameid, playerid),
    FOREIGN KEY (gameid) REFERENCES game_dimension(gameid),
    FOREIGN KEY (teamid) REFERENCES team_dimension(teamid)
)