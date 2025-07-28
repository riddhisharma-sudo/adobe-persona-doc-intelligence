
# ----------------------------
# Stage 1: Base Image
# ----------------------------
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# ----------------------------
# Install system dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Install Python dependencies
# ----------------------------
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Copy Application Files
# ----------------------------
COPY . /app/

# ----------------------------
# Default Command
# ----------------------------
CMD ["python", "main.py"]
