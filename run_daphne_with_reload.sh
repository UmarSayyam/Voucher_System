#!/bin/bash

# Watch the directory for any changes to Python files and restart Daphne when changes are detected
watchmedo auto-restart --directory=./ --pattern="*.py" --recursive -- daphne -b 0.0.0.0 -p 8000 vouchers_system.asgi:application
