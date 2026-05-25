from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import UserProfile
from album.models import Album
from decouple import config


class Command(BaseCommand):
    help = 'Initialize database with admin user and sample data'

    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_password = 'admin123'  # Change this in production!

        if not User.objects.filter(username=admin_username).exists():
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            # Create admin profile
            UserProfile.objects.create(user=admin_user, role='admin')
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Admin user created: username="{admin_username}", password="{admin_password}"'
                )
            )
        else:
            self.stdout.write(self.style.WARNING(f'Admin user already exists'))

        # Create test user if it doesn't exist
        test_username = 'testuser'
        test_email = 'testuser@example.com'
        test_password = 'testuser123'

        if not User.objects.filter(username=test_username).exists():
            test_user = User.objects.create_user(
                username=test_username,
                email=test_email,
                password=test_password
            )
            # Create user profile
            UserProfile.objects.create(user=test_user, role='user')
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Test user created: username="{test_username}", password="{test_password}"'
                )
            )
        else:
            self.stdout.write(self.style.WARNING(f'Test user already exists'))

        # Create sample album if it doesn't exist
        if not Album.objects.filter(name='Sample Album').exists():
            admin_user = User.objects.get(username=admin_username)
            sample_album = Album.objects.create(
                name='Sample Album',
                description='This is a sample album to demonstrate the photo gallery functionality.',
                owner=admin_user,
                is_public=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Sample album created')
            )
        else:
            self.stdout.write(self.style.WARNING(f'Sample album already exists'))

        self.stdout.write(self.style.SUCCESS('\n✓ Database initialization complete!'))
        self.stdout.write('\nTest Credentials:')
        self.stdout.write(f'  Admin - username: "admin", password: "admin123"')
        self.stdout.write(f'  User  - username: "testuser", password: "testuser123"')
