import logging

from django.core.management.base import BaseCommand

from pmoney.catalog.models import Podcast


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Refresh the Planet Money podcast catalog.'

    def handle(self, *args, **options):
        # Start at 1 and increment by 24 episodes at a time until no podcasts come back.
        pass
