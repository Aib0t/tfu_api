FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc libc-dev g++ build-base && \
    pip install -r requirements.txt && pip install gunicorn uvicorn[standard] && \
    apk del .build-deps

COPY ./ .

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=1"
# Error: Invalid ssl_version: 1. Valid options: SSLv23, TLS, TLS_CLIENT, TLS_SERVER, TLSv1, TLSv1_1, TLSv1_2
#CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","main:app"] #,"--certfile=/ssl/server.crt","--keyfile=/ssl/server.key"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--proxy-headers"]
