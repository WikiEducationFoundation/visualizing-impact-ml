import os
import psycopg2
import subprocess

# Database configuration
DB_NAME = "wikivi"

# Connect to the PostgreSQL database
conn = psycopg2.connect(database=DB_NAME)
cursor = conn.cursor()

# Fetch articles from the wikipedia_data table
cursor.execute("SELECT id, parsed_content FROM wikipedia_data;")
articles = cursor.fetchall()

for article_id, content in articles:
    # Tokenize the content to get the first 512 tokens
    tokens = content.split()[:512]
    tokenized_content = " ".join(tokens)

    # Save the tokenized content to a temporary file
    with open("temp.txt", "w") as f:
        f.write(tokenized_content)

    # Use llama.cpp to generate embeddings for the tokenized content
    subprocess.run(["./llama", "embed", "-i", "temp.txt", "-o", "output.vec", "-m", "path_to_openllama_3B_model"])

    # Read the generated embeddings
    with open("output.vec", "r") as f:
        embedding = f.read()

    # Store the embedding in the wikipedia_data table
    cursor.execute("UPDATE wikipedia_data SET embedding_column = %s WHERE id = %s;", (embedding, article_id))

# Apply pgvector on the embedding column
cursor.execute("SELECT setvector(embedding_column) AS vector_output FROM wikipedia_data;")

# Commit the changes to the database
conn.commit()

# Close the database connection
cursor.close()
conn.close()

# Cleanup temporary files
os.remove("temp.txt")
os.remove("output.vec")
