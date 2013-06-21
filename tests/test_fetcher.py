from unittest import TestCase
from requests.exceptions import HTTPError
from podscrape.models import Url
from podscrape.scraper import Scraper
from podscrape.fetcher import Fetcher

test_url = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2"
url_404 = "https://itunes.apple.com/us/stuff/podcasts-arts/id1301?mt=2"

class FetcherTest(TestCase):

    def test_fetch(self):
        fetcher = Fetcher()
        scraper = fetcher.fetch(test_url)

        genre = scraper.get_currently_selected_genre()
        subgenre = scraper.get_currently_selected_subgenre()
        letter = scraper.get_currently_selected_letter()
        page = scraper.get_currently_selected_page()

        self.assertEqual(genre.string, "Arts")
        self.assertEqual(subgenre, None)
        self.assertEqual(letter, None)
        self.assertEqual(page, None)

    def test_404_fetch(self):
        fetcher = Fetcher()
        self.assertRaises(HTTPError, fetcher.fetch, url_404)
