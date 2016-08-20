from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from django.core.management.base import BaseCommand

from pmoney.catalog.models import Podcast
from pmoney.catalog.utils import PlanetMoneyDataLoader


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Refresh the Planet Money podcast catalog.'

    def handle(self, *args, **options):
        # NPR includes 24 podcasts on each page. We start at 1 and increment by
        # 24 episodes at a time until no podcasts come back.
        offsets = range(1, 1000, 24)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(PlanetMoneyDataLoader.ingest, offset) for offset in offsets]

        for future in as_completed(futures):
            for data in future.result():
                title = data.pop('title')
                _, created = Podcast.objects.get_or_create(title=title, defaults=data)

                if created:
                    logger.info('Saved new podcast "%s".', title)
                else:
                    logger.info('Found existing podcast "%s".', title)