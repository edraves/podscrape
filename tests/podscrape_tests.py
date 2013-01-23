from podscrape.scraper import Scraper
from nose.tools import *

first_page_filename = "./tests/itunes_arts_page.html"

def test_make_soup():
    scraper = Scraper(first_page_filename)
    assert_equal(scraper.soup.title.string, "Arts - Podcasts Downloads on iTunes")

#Should be 80x3 = 240
def test_get_itunes_podcast_urls():
    scraper = Scraper(first_page_filename)
    itunes_urls = scraper.get_itunes_podcast_urls()

    assert_equal(len(itunes_urls), 240)
    assert_equal(itunes_urls[0], "https://itunes.apple.com/us/podcast/the-moth-podcast/id275699983?mt=2")

def test_get_top_level_genre_urls():
    scraper = Scraper(first_page_filename)
    genre_urls = scraper.get_top_level_genre_urls()

    assert_equal(len(genre_urls), 16)
    assert_equal(genre_urls[0], "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2")
    assert_equal(genre_urls[1], "https://itunes.apple.com/us/genre/podcasts-business/id1321?mt=2")

def test_get_subgenre_urls():
    scraper = Scraper(first_page_filename)
    subgenre_urls = scraper.get_subgenre_urls()

    assert_equal(len(subgenre_urls), 6)
    assert_equal(subgenre_urls[0], "https://itunes.apple.com/us/genre/podcasts-arts-design/id1402?mt=2")
