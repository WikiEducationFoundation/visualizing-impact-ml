CREATE TABLE wikipedia_data (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    summary TEXT,
    sections TEXT,
    links TEXT
);
