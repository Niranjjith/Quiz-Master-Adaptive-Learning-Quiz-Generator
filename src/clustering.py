from sklearn.cluster import KMeans
import pandas as pd

class DifficultyClustering:
    def __init__(self, n_clusters=3):
        self.model = KMeans(n_clusters=n_clusters, random_state=42)

    def fit(self, df):
        features = df[["accuracy_rate", "avg_time"]]
        df["difficulty"] = self.model.fit_predict(features)
        return df