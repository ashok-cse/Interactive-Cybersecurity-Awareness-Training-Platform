# CyberAware Training Platform – Docker image
# Build: docker build -t cyberaware .
# Run:   docker run -p 5000:5000 --env-file .env cyberaware

FROM python:3.11-slim

# Prevent .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer cached separately from source code)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/docker-entrypoint.sh

# Data directory for the SQLite database (mount a named volume here)
RUN mkdir -p /data

EXPOSE 5000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
