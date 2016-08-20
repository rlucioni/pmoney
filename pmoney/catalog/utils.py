import datetime
import logging

from bs4 import BeautifulSoup
import requests


logger = logging.getLogger(__name__)


class PlanetMoneyDataLoader:
    url = 'http://www.npr.org/podcasts/510289/planet-money/partials?start={}'

    @classmethod
    def ingest(cls, offset=1):
        logger.info('Loading offset %d.', offset)
        response = requests.get(cls.url.format(offset))

        # Although slow, the html5lib parser is good at dealing with the broken HTML
        # used for NPR's podcast listings.
        soup = BeautifulSoup(response.content, 'html5lib')
        articles = soup.find_all(class_='podcast-episode')

        podcasts = []
        for article in articles:
            info = article.find(class_='item-info')

            publication_date = datetime.datetime.strptime(info.time['datetime'], '%Y-%m-%d').date()
            title = info.find(class_='title').string
            
            try:
                teaser = list(info.find(class_='teaser').children)[-1].strip()
            except:
                try:
                    # Some articles have really broken HTML.
                    teaser = info.find_all('p')[1].string
                except:
                    logger.info('Teaser missing for %s.', title)
                    teaser = ''

            try:
                embed_url = info.find(class_='audio-tool-embed').button['data-embed-url']
            except:
                logger.info('Embed URL missing for %s.', title)
                embed_url = ''

            try:
                download_url = info.find(class_='audio-tool-download').a['href']
            except:
                logger.info('Download URL missing for %s.', title)
                download_url = ''

            # Intentionally excluded. Not accurate, and not always provided.
            # duration = info.find(class_='audio-module-duration').string

            podcasts.append({
                'publication_date': publication_date,
                'title': title,
                'teaser': teaser,
                'embed_url': embed_url,
                'download_url': download_url,
            })

        return podcasts
