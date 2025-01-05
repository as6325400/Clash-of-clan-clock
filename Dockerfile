FROM debian:latest

RUN apt update && apt install -y curl python3 python3-pip python3-poetry


ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . ./

RUN poetry install


CMD ["./entrypoint.sh"]

