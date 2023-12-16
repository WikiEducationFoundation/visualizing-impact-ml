import argparse
import psycopg2
import subprocess
import datetime

import datetime
import concurrent.futures

import log_module
from psycopg2 import pool

now = datetime.datetime.now()

llama_logger = log_module.init_logger('llama_output', 'llama_output.log')
print_logger = log_module.init_logger('print_output', 'print_output.log')

parser = argparse.ArgumentParser(description="Embedding params")
parser.add_argument('-e', '--embedding_path', default="/extrastorage/visualizing-impact-ml/llama.cpp/embedding", help="Path to the embeddings")
parser.add_argument('-m', '--model_path', default="/extrastorage/visualizing-impact-ml/llama.cpp/models/open_llama_3b_v2/ggml-model-f16.gguf", help="Path to the model file")
parser.add_argument('-n', '--num_threads', type=int, default=2, help="Number of threads for parallel processing of data")
parser.add_argument('-t', '--thread_count', type=str, default=4, help="Thread count to be used by llama to increase embedding generation speed (different than the threads used for parallel processing)")
parser.add_argument('-l', '--limit', type=int, default=10000, help="Limit the number of articles to process") 
args = parser.parse_args()

conn_pool = psycopg2.pool.SimpleConnectionPool(1, args.num_threads, dbname="wikivi")

def process_article(article_data, args):
    article_id, content = article_data
    try:
        tokens = content.split()[:512]
        tokenized_content = " ".join(tokens)

        process = subprocess.Popen([args.embedding_path, "--log-disable", "-p", "-", "-m", args.model_path, "-t", args.thread_count], 
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        embedding, stderr = process.communicate(tokenized_content)

        if stderr:
            llama_logger.error(stderr)

        embedding_list = [float(value) for value in embedding.split()]
        conn = conn_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("UPDATE wikipedia_data SET embeddings = %s WHERE id = %s;", (embedding_list, article_id))
        cursor.close()
        conn.commit()
    except Exception as e:
        print_logger.error(f"Error processing article {article_id}: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn_pool.putconn(conn)

print_logger.info(f"Article limit set to: {args.limit} articles")

conn = psycopg2.connect(dbname="wikivi")
cursor = conn.cursor()
query = "SELECT id, parsed_content from wikipedia_data where parsed_content not like '%%redirect%%' and embeddings is null limit %s;"
cursor.execute(query, (args.limit,))
articles = cursor.fetchall()
cursor.close()
conn.close()

print_logger.info(f"Running {args.num_threads} threads for parallel processing")
print_logger.info(f"Running {args.thread_count} threads for embedding generation speed")

with concurrent.futures.ThreadPoolExecutor(max_workers=args.num_threads) as executor:
    executor.map(process_article, articles, [args]*len(articles))

conn_pool.closeall()

now2 = datetime.datetime.now()
elapsed = now2 - now
print_logger.info(f"Total elapsed time: {elapsed.total_seconds()} seconds")

