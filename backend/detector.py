import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        X = self.scaler.fit_transform(df)
        self.model.fit(X)
        self.is_fitted = True

    def predict(self, df: pd.DataFrame) -> list[dict]:
        X = self.scaler.transform(df)
        # -1 = anomaly, 1 = normal from IsolationForest
        labels = self.model.predict(X)
        scores = self.model.score_samples(X)

        # Normalize scores to 0-1 anomaly probability (higher = more anomalous)
        min_s, max_s = scores.min(), scores.max()
        if max_s > min_s:
            normalized = 1 - (scores - min_s) / (max_s - min_s)
        else:
            normalized = np.zeros(len(scores))

        return [
            {
                "is_anomaly": bool(labels[i] == -1),
                "anomaly_score": round(float(normalized[i]), 3),
            }
            for i in range(len(labels))
        ]

    def fit_predict(self, df: pd.DataFrame) -> list[dict]:
        self.fit(df)
        return self.predict(df)