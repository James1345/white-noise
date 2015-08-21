from django.core.management.base import BaseCommand, CommandError

class Command(BaseCOmmand):
    help = 'Run white-noise fixtures'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
