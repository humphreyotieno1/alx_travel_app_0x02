from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a test user for API testing'

    def handle(self, *args, **options):
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpass123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Test',
                last_name='User',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Successfully created test user'))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        else:
            self.stdout.write(self.style.WARNING('Test user already exists'))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS('Password: testpass123'))
