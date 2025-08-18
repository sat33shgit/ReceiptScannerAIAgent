FROM python:3.9-slim

WORKDIR /app

COPY requirements_web.txt .
RUN pip install -r requirements_web.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
