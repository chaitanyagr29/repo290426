import requests
import numpy as np
import time
from sklearn.ensemble import IsolationForest

PROM_URL = "http://<prometheus-service>:9090/api/v1/query_range"

def fetch_metrics():
    try:
        end = int(time.time())
        start = end - 300  # last 5 minutes

        response = requests.get(
            PROM_URL,
            params={
                "query": "rate(request_count[1m])",
                "start": start,
                "end": end,
                "step": 5
            },
            timeout=5
        )

        data = response.json()

        values = [
            float(v[1])
            for result in data['data']['result']
            for v in result['values']
        ]

        return values

    except Exception as e:
        print("Error:", e)
        return []


values = fetch_metrics()

if len(values) < 20:
    print("⚠️ Not enough data")
    exit()

X = np.array(values).reshape(-1, 1)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

pred = model.predict(X)

if pred[-1] == -1:
    print("🚨 Anomaly detected!")
else:
    print("✅ System normal")

