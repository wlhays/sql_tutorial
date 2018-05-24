

CREATE TABLE runners (
    id        integer  PRIMARY KEY,
    name      text     NOT NULL,
    birthyear integer  NOT NULL,
    gender    text     NOT NULL,
    location  text
);

CREATE TABLE races (
    id            integer  PRIMARY KEY,
    name          text     NOT NULL,
    sponsor       text,
    distance_km   integer  NOT NULL,
    date          text     NOT NULL,
    location      text
);


CREATE TABLE times (
    id            integer  PRIMARY KEY,
    runner_id     integer  NOT NULL,
    race_id       integer  NOT NULL,
    place         integer,
    time          real     NOT NULL,
    FOREIGN KEY(runner_id) REFERENCES runner(id),
    FOREIGN KEY(race_id) REFERENCES race(id)
);
