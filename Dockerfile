FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ .

# Run the application
EXPOSE 5000
CMD ["python", "app.py"]
