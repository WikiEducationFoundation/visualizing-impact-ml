import pandas as pd
import psycopg2
import umap
import plotly.express as px
import numpy as np

conn = psycopg2.connect(
    dbname='wikivi',
)

query = "SELECT embeddings FROM wikipedia_data where embeddings is not null"
df = pd.read_sql_query(query, conn)

def parse_embedding(s):
    s = s.strip('{}')
    return np.array(s.split(','), dtype=float)

embeddings = np.stack(df['embeddings'].apply(parse_embedding))

reducer = umap.UMAP(random_state=42)
embedding_2d = reducer.fit_transform(embeddings)

fig = px.scatter(x=embedding_2d[:, 0], y=embedding_2d[:, 1], title="UMAP Visualization of Article Embeddings", labels={'x': 'UMAP Dimension 1', 'y': 'UMAP Dimension 2'})
fig.update_traces(marker=dict(size=5))
#fig.savefig('interactive.png')
fig.show()

