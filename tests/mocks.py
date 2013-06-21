from podscrape.scraper import Scraper
class MockFetcher(object):

    def __init__(self, return_values):
        self.return_values = return_values

    def fetch(self, url):
        text = text_from_file(self.return_values[url])
        return Scraper(text)

class MockSingleResultFetcher(object):

    def __init__(self, return_file):
        self.return_text = text_from_file(return_file)

    def fetch(self, url):
        return Scraper(self.return_text)

def text_from_file(filename):
    handle = open(filename)
    text = handle.read()
    handle.close()
    return text
