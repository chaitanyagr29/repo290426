FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 8000
EXPOSE 9090


CMD ["python", "app.py"]
