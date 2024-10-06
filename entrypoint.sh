#!/bin/bash

# Run Gunicorn
exec gunicorn main:app \
    --config gunicorn_conf.py \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8080