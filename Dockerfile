# Use Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the project files
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=task_manager_project.settings
ENV PYTHONPATH=/app

# Create a directory for static files
RUN mkdir -p /app/task_manager_project/staticfiles

# Expose the port
EXPOSE 8000

# Run migrations and start Gunicorn
CMD ["bash", "-c", "python task_manager_project/manage.py migrate && python task_manager_project/manage.py collectstatic --noinput && gunicorn task_manager_project.wsgi:application --bind 0.0.0.0:8000"]