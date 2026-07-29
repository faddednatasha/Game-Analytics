import sqlite3

conn = sqlite3.connect("tennis.db")
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS categories (
    category_id     VARCHAR(50)  PRIMARY KEY,
    category_name   VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS competitions (
    competition_id      VARCHAR(50)  PRIMARY KEY,
    competition_name    VARCHAR(100) NOT NULL,
    parent_id            VARCHAR(50),
    type                 VARCHAR(20)  NOT NULL,
    gender               VARCHAR(10)  NOT NULL,
    level                VARCHAR(30),
    category_id          VARCHAR(50)  NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS complexes (
    complex_id      VARCHAR(50)  PRIMARY KEY,
    complex_name    VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id        VARCHAR(50)  PRIMARY KEY,
    venue_name      VARCHAR(100) NOT NULL,
    city_name       VARCHAR(100) NOT NULL,
    country_name    VARCHAR(100) NOT NULL,
    country_code    CHAR(3)      NOT NULL,
    timezone        VARCHAR(100) NOT NULL,
    complex_id      VARCHAR(50)  NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
);

CREATE TABLE IF NOT EXISTS competitors (
    competitor_id   VARCHAR(50)  PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    country         VARCHAR(100) NOT NULL,
    country_code    CHAR(3)      NOT NULL,
    abbreviation    VARCHAR(10)  NOT NULL
);

CREATE TABLE IF NOT EXISTS competitor_rankings (
    rank_id                 INTEGER      PRIMARY KEY AUTOINCREMENT,
    rank                    INTEGER      NOT NULL,
    movement                INTEGER,
    points                  INTEGER,
    competitions_played     INTEGER,
    competitor_id           VARCHAR(50)  NOT NULL,
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
);
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")