from podscrape.scraper import Scraper
from podscrape.models import Podcast

class MockFetcher(object):

    def __init__(self, return_values):
        self.return_values = return_values

    def fetch(self, url):
        text = text_from_file(self.return_values[url])
        return Scraper(text)

    def batch_lookup(self, urls):
        podcast_list = []
        for url in urls:
            podcast_list.append(Podcast(1, "Title", "http://example.com/rss"))
        return podcast_list

class MockSingleResultFetcher(object):

    def __init__(self, return_file):
        self.return_text = text_from_file(return_file)

    def fetch(self, url):
        return Scraper(self.return_text)

    def batch_lookup(self, urls):
        podcast_list = []
        for url in urls:
            podcast_list.append(Podcast(1, "Title", "http://example.com/rss"))
        return podcast_list

def text_from_file(filename):
    handle = open(filename)
    text = handle.read()
    handle.close()
    return text
