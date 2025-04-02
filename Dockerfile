FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies in the correct order with specific versions
COPY app/requirements.txt .
RUN pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ .

# Run the application
EXPOSE 5000
CMD ["python", "app.py"]
