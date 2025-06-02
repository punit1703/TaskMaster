from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        if os.environ.get('ENVIRONMENT') == 'production':
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'punit'),
                    email=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'pr17032006@gmail.com'),
                    password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass123'),
                )
