FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app .

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]