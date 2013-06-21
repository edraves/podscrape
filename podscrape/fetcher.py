import requests
from podscrape.scraper import Scraper
from podscrape import lookup

class Fetcher(object):
    """
    Handles http requests for outside data
    """

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

    def lookup(self, url):
        """
        Return a Podcast from an iTunes podcast url
        """
        itunes_id = lookup.itunes_id_from_url(url)
        payload = {'id': itunes_id}
        r = requests.get("https://itunes.apple.com/lookup", params=payload)

        r.raise_for_status()
        podcast = lookup.podcast_from_json(r.text)
        return podcast

    def batch_lookup(self, url_list):
        """
        Return a list of Podcasts from a list of iTunes podcast urls
        """
        podcasts = []
        for url in url_list:
            podcasts.append(self.lookup(url))
        return podcasts
