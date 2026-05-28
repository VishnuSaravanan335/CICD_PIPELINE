FROM python:3.11-slim

WORKDIR /app

COPY fintrack/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fintrack/ .

EXPOSE 5000
CMD ["python", "app.py"]
