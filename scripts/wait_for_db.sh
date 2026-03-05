#!/bin/sh
set -e

python - <<'PY'
import os, time
import psycopg

host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "5432"))
name = os.getenv("DB_NAME", "poe")
user = os.getenv("DB_USER", "poe")
password = os.getenv("DB_PASSWORD", "poe")

dsn = f"host={host} port={port} dbname={name} user={user} password={password}"

deadline = time.time() + 60  # 60s timeout
last_err = None

while time.time() < deadline:
    try:
        with psycopg.connect(dsn, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        print("DB is ready")
        raise SystemExit(0)
    except Exception as e:
        last_err = e
        time.sleep(1)

print("DB wait timeout. Last error:", repr(last_err))
raise SystemExit(1)
PY

