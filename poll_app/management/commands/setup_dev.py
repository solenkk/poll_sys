from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Setup development environment'

    def handle(self, *args, **options):
        self.stdout.write('Setting up development environment...')
        
        # Create superuser if not exists
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if username and email and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Created superuser: {username}'))
            else:
                self.stdout.write(f'Superuser {username} already exists')
        
        self.stdout.write(self.style.SUCCESS('Setup complete!'))