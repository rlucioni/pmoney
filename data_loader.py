from bs4 import BeautifulSoup
import requests


class PlanetMoneyDataLoader:
    # Start at 1 and increment by 24 episodes at a time until no articles come back.
    url = 'http://www.npr.org/podcasts/510289/planet-money/partials?start={}'

    def ingest(self, offset=1):
        response = requests.get(url.format(offset))
        soup = BeautifulSoup(response.content, 'html5lib')
        episodes = soup.find_all('article', class_='podcast-episode')

        for episode in episodes:
            info = episode.find(class_='item-info')

            publication_date = info.time['datetime']
            title = info.find(class_='title').string
            teaser = list(info.find(class_='teaser').children)[-1].strip()
            # Intentionally excluded. Not accurate, and not always provided.
            # duration = info.find(class_='audio-module-duration').string
            embedded_url = info.find(class_='audio-tool-embed').button['data-embed-url']
            download_url = info.find(class_='audio-tool-download').a['href']
