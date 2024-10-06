# gunicorn_conf.py

# Number of worker processes for handling requests
workers = 4

# The type of workers to use (Uvicorn workers are required for FastAPI)
worker_class = "uvicorn.workers.UvicornWorker"

# The port to bind to
bind = "0.0.0.0:8080"

# Log level (can be changed to 'debug' for more verbose logging)
loglevel = "info"

# Timeout for each request
timeout = 120