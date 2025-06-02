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

# Copy the project files
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=task_manager_project.settings
ENV PYTHONPATH=/app:/app/task_manager_project

# Expose the port
EXPOSE 8000

# Run migrations and start Gunicorn
CMD ["bash", "-c", "python task_manager_project.manage.py migrate && gunicorn task_manager_project.wsgi:application --bind 0.0.0.0:8000"]



# FROM python:3.11-slim

# ENV PYTHONUNBUFFERED=1

# WORKDIR /app/task_manager_project

# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["gunicorn", "task_manager_project.wsgi:application", "--bind", "0.0.0.0:10000", "--workers", "3"]