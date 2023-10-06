import psycopg2
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

# Database connection parameters
DB_NAME = "wikivi"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
)
cursor = conn.cursor()

# Retrieve the content column
cursor.execute("SELECT id, content FROM wikipedia_data;")
rows = cursor.fetchall()

# Preprocess and tokenize the content
tokenized_data = [simple_preprocess(row[1]) for row in rows]

# Train a Word2Vec model
model = Word2Vec(sentences=tokenized_data, vector_size=100, window=5, min_count=1, workers=4)
model.save("word2vec.model")

# Vectorize the content (for simplicity, we'll use the average of all word vectors in an article)
vectorized_data = []
for tokens in tokenized_data:
    vector = sum([model.wv[token] for token in tokens if token in model.wv.index_to_key]) / len(tokens)
    vectorized_data.append(vector.tolist())

# Add a new column for the vectorized text
cursor.execute("ALTER TABLE wikipedia_data ADD COLUMN vectorized_content float[];")

# Update the table with the vectorized content
for i, row in enumerate(rows):
    cursor.execute("UPDATE wikipedia_data SET vectorized_content = %s WHERE id = %s;", (vectorized_data[i], row[0]))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
