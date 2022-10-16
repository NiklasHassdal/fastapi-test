FROM python:3.10-alpine3.16
ENV PYTHONDONTWRITEBYTECODE=1
RUN apk update
RUN apk add gcc build-base
COPY ./src/requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt
COPY ./src/app/ /src/app/
WORKDIR /src/
CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 80