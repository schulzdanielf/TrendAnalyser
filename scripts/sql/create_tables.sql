CREATE TABLE IF NOT EXISTS trends_data (
    id SERIAL PRIMARY KEY,
    term VARCHAR(255),
    interest FLOAT,
    date TIMESTAMP,
    candidate VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS g1_news (
    id SERIAL PRIMARY KEY,
    link TEXT UNIQUE,
    title TEXT,
    description TEXT,
    date TIMESTAMP,
    text TEXT,
    candidate TEXT
);
