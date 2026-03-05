FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=10

WORKDIR /app

# Install deps first for better layer caching
COPY requirements.txt /app/requirements.txt

# If BuildKit is enabled, this cache mount speeds things up a lot
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip setuptools wheel \
    && pip install --prefer-binary -r /app/requirements.txt


COPY . /app

# Ensure all scripts are executable (especially entrypoint.prod.sh)
RUN chmod +x /app/scripts/*.sh \
    && mkdir -p /app/vol/static /app/vol/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
