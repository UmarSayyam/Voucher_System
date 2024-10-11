# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application files
COPY . /app/

# Add the entrypoint.sh script and give execution permission
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

RUN python manage.py collectstatic --no-input
# Expose the port Django will run on
EXPOSE 8000

# Set Daphne as the entry point to run the ASGI application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "vouchers_system.asgi:application"]
