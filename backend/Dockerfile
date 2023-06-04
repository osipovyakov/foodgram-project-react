FROM python:3.9.0-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]