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



#!/usr/bin/env bash

pip install -r requirements.txt

npm install
python manage.py tailwind install
python manage.py tailwind build

python manage.py migrate
python manage.py collectstatic --noinput
