# Import necessary modules to set up Django environment
import os
from django.core.wsgi import get_wsgi_application
import django

# Set up Django environment
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticker_new.settings')
application = get_wsgi_application()

# Import the required management command modules
from django.core.management.base import BaseCommand
from datetime import datetime
from polls.models import Ticker_Extraction_Model

# Define the management command class
class Command(BaseCommand):
    help = 'Update existing time data'

    def handle(self, *args, **options):
        # Iterate through all objects
        for obj in Ticker_Extraction_Model.objects.all():
            # Convert the existing time string to a TimeField
            if obj.time:
                try:
                    # Parse the time string and convert it to a datetime object
                    time_obj = datetime.strptime(obj.time, "%I:%M %p").time()
                    obj.time = time_obj
                    obj.save()
                except ValueError:
                    # Handle parsing errors if the time string is not in the expected format
                    pass

        self.stdout.write(self.style.SUCCESS('Successfully updated time data'))
