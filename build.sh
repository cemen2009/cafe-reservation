#!/usr/bin/env bash
# Exit on enter
set -o errexit

# modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# convert static asserts to files
python manage.py collectstatic --noinput -v 0

# apply any outstanding database migrations
python manage.py migrate