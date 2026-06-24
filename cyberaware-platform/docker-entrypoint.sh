#!/bin/bash
# CyberAware Training Platform – container entrypoint
# Runs DB initialisation, optional seeding, then starts Gunicorn.
set -e

echo "[entrypoint] Initialising database …"
python db_init.py

if [ "${SEED_ON_START}" = "true" ]; then
    echo "[entrypoint] SEED_ON_START=true – seeding demo data …"
    python seed.py
fi

echo "[entrypoint] Starting Gunicorn on 0.0.0.0:${PORT:-5000} …"
exec gunicorn run:app \
    --bind "0.0.0.0:${PORT:-5000}" \
    --workers "${GUNICORN_WORKERS:-2}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
