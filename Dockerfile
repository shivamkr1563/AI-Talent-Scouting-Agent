FROM python:3.10-slim

# Set working directory
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Create logs directory
RUN mkdir -p /app/backend/logs

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "main_v2:app", "--host", "0.0.0.0", "--port", "8000"]
