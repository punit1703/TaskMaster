#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Install Tailwind dependencies
npm install
python manage.py tailwind install
python manage.py tailwind build

# DB and static setup
python manage.py migrate
python manage.py collectstatic --noinput
