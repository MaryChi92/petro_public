import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Create a database dump and save it to json'

    def handle(self, *args, **options):
        current_datetime = datetime.datetime.now()
        date_string = current_datetime.strftime("%Y%m%d%H%M%S")
        filename = f"db{date_string}.json"

        with open(filename, 'w') as file:
            call_command(
                'dumpdata',
                exclude=['admin.logentry',
                         'auth.permission',
                         'contenttypes.contenttype',
                         'sessions.session',
                         'cookie_consent.logitem'],
                indent=2,
                stdout=file
            )

        self.stdout.write(self.style.SUCCESS('Database dump has been created and saved to json.'))
