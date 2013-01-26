from podscrape.scraper import Scraper
class MockFetcher(object):

    def __init__(self, return_values):
        self.return_values = return_values

    def fetch(self, url):
        return Scraper(self.return_values[url])
