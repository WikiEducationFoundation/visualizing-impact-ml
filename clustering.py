import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import umap
import psycopg2
import pandas as pd

conn = psycopg2.connect(dbname='wikivi')

query = "SELECT embeddings from wikipedia_data"
df = pd.read_sql_query(query, conn)
embeddings = np.array(df['embeddings'].tolist()) # check if this works

k = 100
kmeans = KMeans(n_clusters=k, random_state=0)

reducer = umap.UMAP()
embedding_2d = reducer.fit_transform(embeddings)

#plt.figure()
#fill in more later
