from nose.tools import *
from tests.mocks import MockFetcher
from podscrape.driver import Driver

test_url = "http://itunes.apple.com/genre/podcasts-arts/id1301?mt=2"
test_url2 = "http://itunes.apple.com/genre/podcasts-arts/id1301?mt=2&letter=A"
test_url3 = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2&letter=C&page=4#page"
test_url_file = "./tests/itunes_arts_page.html"

def test_parse_url():
    driver = Driver(test_url)
    letter, page = driver.parse_url(test_url)
    assert_equal(letter, '')
    assert_equal(page, 0)

    letter, page = driver.parse_url(test_url2)
    assert_equal(letter, 'A')
    assert_equal(page, 1)

    letter, page = driver.parse_url(test_url3)
    assert_equal(letter, 'C')
    assert_equal(page, 4)

#def test_starting_point():
#    driver = Driver(test_url, MockFetcher(test_url_file))
#    assert_equal(driver.current_letter, '')
#    assert_equal(driver.current_genre.text, "Arts")
    

#    next_url = stuff.next_page()
#    assert_equal(next_url, test_url)

    #next_url = stuff.next_page()
    #assert_equal(next_url, test_url2)
    
#def test_next_genre():
#    driver = Driver(test_url)
#    driver.fetcher = MockFetcher(test_url_file)

"""
Driver notes
Driver(url)
start from that url, get genre list, subgenre list, then scrape popular, and continue from the start of the currently selected genre.

Driver(url)
if url includes a letter, start from that letter and move through. numerically, then alphabetically.

if url includes a page number, start at that page, then continue through.
"""

"""
Other potential classes
Fetcher. Fetcher takes a url and returns a scraper
or takes a url and returns a json
fetcher.fetch(url)
fetcher.lookup(url)

Rate Limiter
"""
