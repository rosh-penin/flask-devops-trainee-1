FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY main.py .
CMD ["gunicorn","main:app","--bind","0:8080"]
