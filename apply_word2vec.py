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
cursor.execute("SELECT id, parsed_content FROM wikipedia_data;")
rows = cursor.fetchall()

# Preprocess and tokenize the content
#tokenized_data = [simple_preprocess(row[1]) for row in rows]

# Train a Word2Vec model
#model = Word2Vec(sentences=tokenized_data, vector_size=100, window=5, min_count=1, workers=4)
#model.save("word2vec.model")

# Try existing Word2Vec model trained on English Wiki
model = KeyedVectors.load_word2vec_format('model.bin', binary=True)
model.save("word2vec.model")

# Add column for the average vector of the content in each article
cursor.execute("ALTER TABLE wikipedia_data ADD COLUMN avg_vectors float[];")

# Vectorize the parsed content

for row in rows:
    record_id, content = row
    words = content.split()
    vectors = [model[word] for word in words if word in model.key_to_index]

    if not vectors:
        continue

    avg_vector = np.mean(vectors, axis=0)
    cursor.execute("UPDATE wikipedia_data SET avg_vectors = %s WHERE id = %s;", (avg_vector, record_id))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
