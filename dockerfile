FROM python:3.8-slim

RUN pip install --no-cache-dir fastapi uvicorn pymysql jinja2 requests python-multipart

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
