from flask import Flask
from prometheus_client import start_http_server, Counter
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('request_count', 'Total Requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "AIOps CI/CD Running"

if __name__ == "__main__":
    start_http_server(8000)  # Prometheus metrics
    app.run(host="0.0.0.0", port=5000)
