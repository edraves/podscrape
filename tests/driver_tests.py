from nose.tools import *
from bs4 import BeautifulSoup
from tests.mocks import MockFetcher
from podscrape.driver import Driver, parse_url

test_url = "http://itunes.apple.com/genre/podcasts-arts/id1301?mt=2"
test_url2 = "http://itunes.apple.com/genre/podcasts-arts/id1301?mt=2&letter=A"
test_url3 = "https://itunes.apple.com/us/genre/podcasts-society-culture/id1324?mt=2&letter=N&page=2#page"
test_url_file = "./tests/itunes_arts_page.html"
test_url2_file = "./tests/itunes_arts_page_letter_a.html"
test_url3_file = "./tests/itunes_society_and_culture_n_2.html"
fetch_values = {
    test_url: test_url_file,
    test_url2: test_url2_file,
    test_url3: test_url3_file
}

def test_parse_url():
    letter, page = parse_url(test_url)
    assert_equal(letter, '')
    assert_equal(page, 0)

    letter, page = parse_url(test_url2)
    assert_equal(letter, 'A')
    assert_equal(page, 1)

    letter, page = parse_url(test_url3)
    assert_equal(letter, 'N')
    assert_equal(page, 2)    

#def test_starting_point():
#    driver = Driver(test_url, MockFetcher(fetch_values))
#    assert_equal(driver.current_letter, '')
#    assert_equal(driver.current_genre.text, "Arts")
    

#    next_url = stuff.next_page()
#    assert_equal(next_url, test_url)

    #next_url = stuff.next_page()
    #assert_equal(next_url, test_url2)
    
def test_next_genre():
    driver = Driver(test_url, MockFetcher(fetch_values))
    genre = driver.next_genre()
    assert_equal(genre.text, "Business")
    genre = driver.next_genre()
    assert_equal(genre.text, "Comedy")
    genre = driver.next_genre()
    assert_equal(genre.text, "Education")
    genre = driver.next_genre()
    assert_equal(genre.text, "Games & Hobbies")
    genre = driver.next_genre()
    assert_equal(genre.text, "Government & Organizations")
    genre = driver.next_genre()
    assert_equal(genre.text, "Health")
    genre = driver.next_genre()
    assert_equal(genre.text, "Kids & Family")
    genre = driver.next_genre()
    assert_equal(genre.text, "Music")
    genre = driver.next_genre()
    assert_equal(genre.text, "News & Politics")
    genre = driver.next_genre()
    assert_equal(genre.text, "Religion & Spirituality")
    genre = driver.next_genre()
    assert_equal(genre.text, "Science & Medicine")
    genre = driver.next_genre()
    assert_equal(genre.text, "Society & Culture")
    genre = driver.next_genre()
    assert_equal(genre.text, "Sports & Recreation")
    genre = driver.next_genre()
    assert_equal(genre.text, "TV & Film")
    genre = driver.next_genre()
    assert_equal(genre.text, "Technology")
    genre = driver.next_genre()
    assert_equal(genre, None)

def test_next_genre_from_middle():
    driver = Driver(test_url3, MockFetcher(fetch_values))
    genre = driver.next_genre()
    assert_equal(genre.text, "Sports & Recreation")

"""
Driver notes
Driver(url)
start from that url, get genre list, subgenre list, then scrape popular, and continue from the start of the currently selected genre.

Driver(url)
if url includes a letter, start from that letter and move through. numerically, then alphabetically.

if url includes a page number, start at that page, then continue through.

Other potential classes
Fetcher. Fetcher takes a url and returns a scraper
or takes a url and returns a json
fetcher.fetch(url)
fetcher.lookup(url)

Rate Limiter
"""
