FROM python:3.8-alpine AS base
LABEL description="Python3.8,flask-app"
WORKDIR /app
COPY app .
RUN pip install -r requirements.txt && pip install gunicorn
EXPOSE 80

ENTRYPOINT ["gunicorn", "-b", ":80", "app:create_app()"]


