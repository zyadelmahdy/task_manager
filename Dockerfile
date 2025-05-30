# Use Python base image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Install wait-for-it script
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copy requirements and install dependencies early (layer caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Make wait script executable
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=task_manager_project.settings

# Expose the port Django will use
EXPOSE 8000

# Command to run Gunicorn
CMD ["gunicorn", "task_manager_project.wsgi:application", "--bind", "0.0.0.0:8000"]