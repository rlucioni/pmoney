import datetime

from bs4 import BeautifulSoup
import requests


class PlanetMoneyDataLoader:
    url = 'http://www.npr.org/podcasts/510289/planet-money/partials?start={}'

    @classmethod
    def ingest(cls, offset=1):
        response = requests.get(cls.url.format(offset))

        # Although slow, the html5lib parser is good at dealing with the broken HTML
        # used for NPR's podcast listings.
        soup = BeautifulSoup(response.content, 'html5lib')
        articles = soup.find_all(class_='podcast-episode')

        podcasts = []
        for articles in articles:
            info = articles.find(class_='item-info')

            # TODO: Create model instances or leave that to the caller? The latter facilitates threading.
            publication_date = datetime.datetime.strptime(info.time['datetime'], '%Y-%m-%d')
            title = info.find(class_='title').string
            teaser = list(info.find(class_='teaser').children)[-1].strip()
            embed_url = info.find(class_='audio-tool-embed').button['data-embed-url']
            download_url = info.find(class_='audio-tool-download').a['href']

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
