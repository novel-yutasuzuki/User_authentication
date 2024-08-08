FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app .

# CMD ["gunicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]