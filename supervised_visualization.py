import pandas as pd
import psycopg2
import umap
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname='wikivi',
)

query = "SELECT embeddings FROM wikipedia_data where embeddings is not null"
df = pd.read_sql_query(query, conn)

def parse_embedding(s):
    s = s.strip('{}')
    return np.array(s.split(','), dtype=float)

embeddings = np.stack(df['embeddings'].apply(parse_embedding))

reducer = umap.UMAP(random_state=42, n_neighbors=10)
embedding_2d = reducer.fit_transform(embeddings)

plt.figure()
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], cmap='Spectral', s=5, alpha=0.25)
#fig.update_traces(marker=dict(size=5))
plt.savefig('umap_only_10neighbors.png')
plt.show()

