import argparse
import os
import psycopg2
import subprocess
import datetime
import numpy as np

import datetime
import concurrent.futures

import log_module

llama_logger = log_module.init_logger('llama_output', 'llama_output.log')
print_logger = log_module.init_logger('print_output', 'print_output.log')

def process_article(article_data, args):
    article_id, content = article_data
    try:
        tokens = content.split()[:512]
        tokenized_content = " ".join(tokens)

        process = subprocess.Popen([args.embedding_path, "--log-disable", "-p", "-", "-m", args.model_path], 
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        embedding, stderr = process.communicate(tokenized_content)

        if stderr:
            llama_logger.error(stderr)

        embedding_list = [float(value) for value in embedding.split()]
        conn = psycopg2.connect(dbname="wikivi")
        cursor = conn.cursor()
        cursor.execute("UPDATE wikipedia_data SET embeddings = %s WHERE id = %s;", (embedding_list, article_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print_logger.error(f"Error processing article {article_id}: {e}")

now = datetime.datetime.now()

parser = argparse.ArgumentParser(description="Embedding params")
parser.add_argument('-e', '--embedding_path', default="/extrastorage/visualizing-impact-ml/llama.cpp/embedding", help="Path to the embeddings")
parser.add_argument('-m', '--model_path', default="/extrastorage/visualizing-impact-ml/llama.cpp/models/open_llama_3b_v2/ggml-model-f16.gguf", help="Path to the model file")
parser.add_argument('-n', '--num_threads', type=int, default=3, help="Number of threads for parallel processing")

args = parser.parse_args()

conn = psycopg2.connect(dbname="wikivi")
cursor = conn.cursor()
cursor.execute("SELECT id, parsed_content from wikipedia_data where parsed_content not like '%redirect%' and embeddings is null limit 10000;")
articles = cursor.fetchall()
cursor.close()
conn.close()

print_logger.info(f"Running on {args.num_threads} threads")
with concurrent.futures.ThreadPoolExecutor(max_workers=args.num_threads) as executor:
    executor.map(process_article, articles, [args]*len(articles))

now2 = datetime.datetime.now()
elapsed = now2 - now
print_logger.info(f"Total elapsed time: {elapsed.total_seconds()} seconds")

