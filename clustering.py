import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import umap
import psycopg2
import pandas as pd

conn = psycopg2.connect(dbname='wikivi')

query = "SELECT embeddings from wikipedia_data where embeddings not like '%None%' "
df = pd.read_sql_query(query, conn)

def parse_embedding(s):
    s = s.strip('{}')
    return np.array(s.split(','), dtype=float)

embeddings = np.stack(df['embeddings'].apply(parse_embedding))
scaler = StandardScaler()
scaled_embeddings = scaler.fit_transform(embeddings)
pca = PCA(n_components=1000)
reduced_embeddings = pca.fit_transform(scaled_embeddings)

k = 5
kmeans = KMeans(n_clusters=k, init='k-means++', random_state=0, max_iter=500, n_init=10, tol=1e-4)
clusters = kmeans.fit_predict(embeddings)

reducer = umap.UMAP()
embedding_2d = reducer.fit_transform(embeddings)

plt.figure()
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], c=clusters, cmap='Spectral', s=5)
plt.colorbar()
plt.savefig('firsttest_20clusters.png', dpi=300)
plt.close()
