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
    assert_equal(itunes_urls[0].get("href"), "https://itunes.apple.com/us/podcast/the-moth-podcast/id275699983?mt=2")
