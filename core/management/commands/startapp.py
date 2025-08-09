from django.core.management.commands.startapp import Command as StartAppCommand
import os
from django.core.management.base import CommandError


class Command(StartAppCommand):
    help = "Creates a new app inside the 'apps/' directory, creating 'apps/' if it doesn't exist."

    def add_arguments(self, parser):
        # Add app_name argument
        parser.add_argument('app_name', type=str, help="Name of the app to create")
        # Include optional app directory argument
        parser.add_argument(
            '--directory',
            type=str,
            help='Specify the directory where the app should be created',
        )

    def handle(self, *args, **options):
        # Fetch app name and directory
        app_name = options.pop('app_name', None)
        if not app_name:
            raise CommandError("You must provide an application name.")

        # Set default directory to 'apps/'
        apps_dir = "apps"
        target_dir = os.path.join(apps_dir, app_name)
    
        # Use --directory if provided
        custom_directory = options.get('directory')
        if custom_directory:
            target_dir = os.path.join(custom_directory, app_name)

        # Create 'apps/' directory if it doesn't exist
        if not os.path.exists(apps_dir):
            os.makedirs(apps_dir)
            self.stdout.write(self.style.SUCCESS(f"Created '{apps_dir}/' directory."))

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Check if the app already exists
        if os.listdir(target_dir):  # Check if directory is not empty
            raise CommandError(f"App '{app_name}' already exists in '{target_dir}'.")
        
        migrations_dir = os.path.join(target_dir, 'migrations')
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
            init_file = os.path.join(migrations_dir, '__init__.py')
            with open(init_file, 'w') as f:
                f.write('') 
            
            self.stdout.write(self.style.SUCCESS(f"Created '{migrations_dir}/' directory."))

            
        # Define the files to be created by startapp
        files_to_create = [
            'admin.py', 'apps.py', 'models.py', 'tests.py', 'views.py','urls.py',
            'forms.py','serializers.py'
        ]


        # Call the original 'startapp' command without the 'template' option
        # super().handle(*args, **options)
        for file_name in files_to_create:
            file_path = os.path.join(target_dir, file_name)
            with open(file_path, 'w') as f:
                f.write('')  # Empty content for now
            self.stdout.write(self.style.SUCCESS(f"Created {file_name} in '{target_dir}/'"))


        self.stdout.write(self.style.SUCCESS(f"App '{app_name}' created in '{target_dir}/'."))

