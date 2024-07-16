#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from datetime import datetime
from django.conf import settings

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMS.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def log_file(string):
    if settings.DEBUG:
        with open('log.txt', 'a') as f:
            f.write(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] {string} \n')
        

if __name__ == '__main__':
    main()
