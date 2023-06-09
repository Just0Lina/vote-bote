CREATE TABLE IF NOT EXISTS USERS (
    ID Integer UNIQUE NOT NULL,
    USERNAME VARCHAR (20) NOT NULL,
    CAMPUS VARCHAR (20) NOT NULL,
    ROLE VARCHAR(20) NOT NULL,
    TRIBE VARCHAR(20) NOT NULL,
    TAGS text[]
);

CREATE TABLE IF NOT EXISTS VOTES (
    ID serial PRIMARY KEY,
    AUTHOR Integer,
    HEADER TEXT,
    QUESTIONS Integer[],
    TAGS text[]
);

CREATE TABLE IF NOT EXISTS VOTE_TAGS (
    TAG TEXT UNIQUE NOT NULL,
    ROLE VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS TRIBES (
    CAMPUS VARCHAR (20) UNIQUE NOT NULL,
    STUDENTS_LIST text[],
    ABITURIENTS_LIST text[]
);
