"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError

# OperationalError - error, that Django throws when database in not ready.
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        # stdout - standard output
        # we can use it to log things to the screen as our command is executing
        # this just shows in the console the message "Waiting for database".
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                # if database isn't ready, it raises an exception
                # if database is ready -  loop will finish
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
