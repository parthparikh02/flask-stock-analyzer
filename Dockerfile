FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["gunicorn", "-c", "gunicorn_config.py", "run:app"]

