CREATE TABLE wikipedia_data (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT,
    sections TEXT,
    links TEXT
);
