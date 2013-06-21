import requests
from podscrape.scraper import Scraper

class Fetcher(object):

    def fetch(self, url):
        """
        Get a url, Return a Scraper of the page

        Raises:
            HTTPError: if status code is not HTTP 200 OK
        """
        r = requests.get(url)

        if r.status_code != 200:
            r.raise_for_status()
        scraper = Scraper(r.text)
        return scraper
