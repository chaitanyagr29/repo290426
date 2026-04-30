import requests
import numpy as np
from sklearn.ensemble import IsolationForest

PROM_URL = "http://stable-kube-prometheus-sta-prometheus:9090/api/v1/query"

def fetch_metrics():
    try:
        response = requests.get(
            PROM_URL,
            params={"query": "rate(request_count[1m])"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        return [float(v['value'][1]) for v in data['data']['result']]

    except Exception as e:
        print("Error:", e)
        return []

values = fetch_metrics()

if len(values) < 50:
    print("Insufficient data")
    exit()

X = np.array(values).reshape(-1, 1)

model = IsolationForest(contamination="auto", random_state=42)
model.fit(X)

pred = model.predict(X)

if pred[-1] == -1:
    print("🚨 Anomaly detected!")
