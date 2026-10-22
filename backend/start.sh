#!/usr/bin/env bash
set -e

# Run database migrations
echo "==> Running Alembic migrations..."
alembic upgrade head || echo "==> Alembic upgrade warning (tables will be verified by SQLAlchemy)"

# Start Celery worker + beat only if REDIS_URL is configured
if [ -n "$REDIS_URL" ]; then
  echo "==> Starting Celery worker & beat..."
  celery -A celery_app:celery_app worker --beat --concurrency=1 -s /tmp/celerybeat-schedule --loglevel=info &
else
  echo "==> REDIS_URL not set. Skipping background Celery worker (configure REDIS_URL to enable recurring posts)."
fi

# Launch FastAPI web application
echo "==> Starting Uvicorn on port ${PORT:-10000}..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}
