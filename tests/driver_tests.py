from nose.tools import *
from bs4 import BeautifulSoup
from tests.mocks import MockFetcher
from podscrape.driver import Driver, parse_url
from podscrape.scraper import Scraper

test_url = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2"
test_url2 = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2&letter=A"
test_url3 = "https://itunes.apple.com/us/genre/podcasts-society-culture/id1324?mt=2&letter=N&page=2#page"
test_url4 = "https://itunes.apple.com/us/genre/podcasts-music/id1310?mt=2"
test_url5 = "https://itunes.apple.com/us/genre/podcasts-arts-food/id1306?mt=2"

test_url_file = "./tests/itunes_arts_page.html"
test_url2_file = "./tests/itunes_arts_page_letter_a.html"
test_url3_file = "./tests/itunes_society_and_culture_n_2.html"
test_url4_file = "./tests/itunes_music_page.html"
test_url5_file = "./tests/itunes_arts_food_page.html"
fetch_values = {
    test_url: test_url_file,
    test_url2: test_url2_file,
    test_url3: test_url3_file,
    test_url4: test_url4_file,
    test_url5: test_url5_file
}

def test_parse_url():
    letter, page = parse_url(test_url)
    assert_equal(letter, None)
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

def test_next_subgenre():
    driver = Driver(test_url, MockFetcher(fetch_values))
    assert_equal(driver.current_genre.string, "Arts")
    assert_equal(driver.current_subgenre, None)

    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Design")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Fashion & Beauty")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Food")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Literature")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Performing Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Visual Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre, None)

def test_next_subgenre_music():
    driver = Driver(test_url4, MockFetcher(fetch_values))
    assert_equal(driver.current_genre.string, "Music")
    assert_equal(driver.current_subgenre, None)

    subgenre = driver.next_subgenre()
    assert_equal(subgenre, None)

def test_next_subgenre_from_middle():
    driver = Driver(test_url5, MockFetcher(fetch_values))
    assert_equal(driver.current_genre.string, "Arts")
    assert_equal(driver.current_subgenre.string, "Food")

    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Literature")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Performing Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.text, "Visual Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre, None)

def test_next_letter():
    driver = Driver(test_url, MockFetcher(fetch_values))

    for let in "ABCDEFGHIJKLMNOPQRSTUVWXYZ#":
        assert_equal(driver.next_letter(), let)

    assert_equal(driver.next_letter(), None)
    assert_equal(driver.next_letter(), "A")

def test_next_letter_from_middle():
    driver = Driver(test_url3, MockFetcher(fetch_values))
    letter = driver.next_letter()
    assert_equal(letter, "O")

#def test_next_url():
#    driver = Driver(test_url, MockFetcher(fetch_values))
#    assert_equal(driver.next_url(), test_url2)

#    expected_url = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2&letter=A&page=2#page"
#    assert_equal(driver.next_url(), expected_url)
#def test_starting_state():
#    driver = Driver(test_url2, MockFetcher(fetch_values))
#    assert_equal(driver.letters[0].string, "A")
#    assert_equal(driver.pages[0].string, "2")

#    driver = Driver(test_url3, MockFetcher(fetch_values))
#    assert_equal(driver.letters[0].string, "N")
#    assert_equal(driver.pages[0].string, "2")

def test_print_urls():
    driver = Driver(test_url, MockFetcher(fetch_values))
    #TODO Start here. Print the urls to a file.
    driver.output_file = "./tests/output"
    f = open(driver.output_file, 'w')
    f.truncate()
    f.close()
    scraper = Scraper(test_url_file)
    url_list = scraper.get_itunes_podcast_urls()
    source_url = test_url
    genre = "Arts"
    subgenre = None
    driver.write_urls_to_file(source_url, genre, subgenre, url_list)

    f = open(driver.output_file)
    text = f.read()
    f.close()
    split_text = text.split("\t")
    assert_equal(split_text[0], source_url)
    assert_equal(split_text[1], genre)
    assert_equal(split_text[2], "none")
    assert_equal(split_text[3], "Popular")
    assert_equal(split_text[4], "0")
    assert_equal(split_text[5], "https://itunes.apple.com/us/podcast/the-moth-podcast/id275699983?mt=2")
    assert_equal(split_text[-1], "https://itunes.apple.com/us/podcast/darker-projects-byron-chronicles/id160067986?mt=2\n")
    assert_equal(len(split_text), 245)
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
