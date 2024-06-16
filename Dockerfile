FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Configure Poetry
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy the rest of the application files
COPY . /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask application
CMD ["sh", "-c", "sleep 10 && poetry run alembic upgrade head && poetry run python app.py"]
