#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Print debugging info
    print("Current directory:", os.getcwd())
    print("Directory contents:", os.listdir())
    
    # Add the project directory to Python's sys.path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_manager_project"))
    
    # Print Python path
    print("Python path:", sys.path)
    
    # Set Django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager_project.settings")
    
    # Import Django and run the webserver
    try:
        import django
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        
        # Import task_manager_app to verify it's found
        import task_manager_app
        print("Successfully imported task_manager_app")
        
        # Return the application for Gunicorn
        print("Application ready")
    except ImportError as e:
        print(f"Import error: {e}")
        sys.exit(1)