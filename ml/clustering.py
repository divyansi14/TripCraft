import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv("../data/places.csv")

coords = df[['lat', 'lon']]
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(coords)

score = silhouette_score(coords, df['cluster'])
print("Silhouette Score:", score)