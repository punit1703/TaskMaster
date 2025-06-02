#!/usr/bin/env bash

pip install -r requirements.txt

npm install
python manage.py tailwind install
python manage.py tailwind build

python manage.py migrate
python manage.py collectstatic --noinput
