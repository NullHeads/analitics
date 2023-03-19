FROM python:3.10

WORKDIR /app

ENV TZ Europe/Moscow

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --ignore-installed

COPY Docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT /app/entrypoint.sh

COPY Docker/.env /app/.env
COPY . /app