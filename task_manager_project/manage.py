#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Dynamically choose settings based on whether you're on Render or local
    if "RENDER" in os.environ:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_project.task_manager.settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_project.task_manager_project.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()