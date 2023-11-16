CREATE TABLE wikipedia_data (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    parsed_content TEXT,
    embeddings TEXT,
    summary TEXT,
    sections TEXT,
    links TEXT
);
