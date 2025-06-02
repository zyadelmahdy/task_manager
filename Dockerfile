# Use Python base image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies early (layer caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Set Python path explicitly
ENV PYTHONPATH=/app:/app/task_manager_project

# Make wait script executable
RUN chmod +x /app/wait-for-db.sh

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=task_manager_project.settings

# Expose the port Django will use
EXPOSE 8000

# Change into the correct directory
WORKDIR /app/task_manager_project

# Command to run Gunicorn with proper module path
CMD ["sh", "-c", "ls -la task_manager_project/ && gunicorn task_manager_project.wsgi:application --bind 0.0.0.0:8000"]