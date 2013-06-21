from unittest import TestCase
from requests.exceptions import HTTPError
from podscrape.models import Url
from podscrape.scraper import Scraper
from podscrape.fetcher import Fetcher
from tests.mocks import text_from_file

test_url = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2"
url_404 = "https://itunes.apple.com/us/stuff/podcasts-arts/id1301?mt=2"
test_file = "./tests/testcases/itunes_arts_page.html"
lookup_url = "https://itunes.apple.com/us/podcast/npr-all-songs-considered-podcast/id79687345"
lookup_url2 = "https://itunes.apple.com/us/podcast/new-yorker-fiction/id256945396?mt=2"

class TestFetcher(TestCase):

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

    def test_lookup(self):
        fetcher = Fetcher()
        cast = fetcher.lookup(lookup_url)

        self.assertEqual(79687345, cast.itunes_id)

    def test_batch_lookup(self):
        fetcher = Fetcher()
        lookup_urls = [lookup_url, lookup_url2]
        cast_list = fetcher.batch_lookup(lookup_urls)

        self.assertEqual(79687345, cast_list[0].itunes_id)
        self.assertEqual(256945396, cast_list[1].itunes_id)

