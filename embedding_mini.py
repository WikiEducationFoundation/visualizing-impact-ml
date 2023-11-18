import argparse
import os
import psycopg2
import subprocess
import datetime
import numpy as np

now = datetime.datetime.now()

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument('-e', '--embedding_path', default="/extrastorage/visualizing-impact-ml/llama.cpp/embedding", help="Path to the embeddings")
parser.add_argument('-m', '--model_path', default="/extrastorage/visualizing-impact-ml/llama.cpp/models/open_llama_3b_v2/ggml-model-f16.gguf", help="Path to the model file")
args = parser.parse_args()

conn = psycopg2.connect(dbname="wikivi")
cursor = conn.cursor()
cursor.execute("SELECT id, parsed_content from wikipedia_data where parsed_content not like '%redirect%' limit 10000;")
articles = cursor.fetchall()

for article_id, content in articles:
    tokens = content.split()[:512]
    tokenized_content = " ".join(tokens)
    with open("temp.txt", "w") as f:
        f.write(tokenized_content)
    subprocess.run([args.embedding_path, "--log-disable", "-p", "temp.txt", "-m", args.model_path], stdout=open('output.vec', 'w'))
    with open("output.vec", "r") as f:
        embedding = f.read()
    embedding_list = [float(value) for value in embedding.split()]
    cursor.execute("UPDATE wikipedia_data SET embeddings = %s WHERE id = %s;", (embedding_list, article_id))
    conn.commit()

cursor.close()
conn.close()
os.remove("temp.txt")
os.remove("output.vec")

now2 = datetime.datetime.now()
elapsed = now2 - now
print(elapsed.total_seconds())

