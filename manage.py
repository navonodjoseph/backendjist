#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendjist.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    ## added line 18
    port = int(os.environ.get('PORT', 5000))
    
    # commented out line 21
    # execute_from_command_line(sys.argv)

    #added line 24-5
    if len(sys.argv) > 1 and sys.argv[1] =='runserver':
        sys.argv.append('0.0.0.0:{}'.format(port))

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
