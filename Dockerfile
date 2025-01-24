# Use a lightweight Python base image compatible with ARM and other architectures
# "python:3.X-slim" will dynamically adapt to the system architecture
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a working directory for the application
WORKDIR /app

# Install system dependencies for common Python libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    portaudio19-dev \
    python3-twilio \
    python3-dotenv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose a port if your application requires it (optional)
# EXPOSE 8000

# Define the command to run your application (replace as needed)
CMD ["python", "main.py"]

