from nose.tools import *
from bs4 import BeautifulSoup
from tests.mocks import MockFetcher, MockSingleResultFetcher, text_from_file
from podscrape.driver import Driver
from podscrape.scraper import Scraper
from podscrape.output import NullOutput

test_url = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2"
test_url2 = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2&letter=A"
test_url3 = "https://itunes.apple.com/us/genre/podcasts-society-culture/id1324?mt=2&letter=N&page=2#page"
test_url4 = "https://itunes.apple.com/us/genre/podcasts-music/id1310?mt=2"
test_url5 = "https://itunes.apple.com/us/genre/podcasts-arts-food/id1306?mt=2"

test_url_file = "./tests/testcases/itunes_arts_page.html"
test_url2_file = "./tests/testcases/itunes_arts_page_letter_a.html"
test_url3_file = "./tests/testcases/itunes_society_and_culture_n_2.html"
test_url4_file = "./tests/testcases/itunes_music_page.html"
test_url5_file = "./tests/testcases/itunes_arts_food_page.html"
fetch_values = {
    test_url: test_url_file,
    test_url2: test_url2_file,
    test_url3: test_url3_file,
    test_url4: test_url4_file,
    test_url5: test_url5_file
}

def test_next_genre():
    driver = Driver(test_url, MockFetcher(fetch_values))
    driver.populate_state()
    genre = driver.next_genre()
    assert_equal(genre.string, "Business")
    genre = driver.next_genre()
    assert_equal(genre.string, "Comedy")
    genre = driver.next_genre()
    assert_equal(genre.string, "Education")
    genre = driver.next_genre()
    assert_equal(genre.string, "Games & Hobbies")
    genre = driver.next_genre()
    assert_equal(genre.string, "Government & Organizations")
    genre = driver.next_genre()
    assert_equal(genre.string, "Health")
    genre = driver.next_genre()
    assert_equal(genre.string, "Kids & Family")
    genre = driver.next_genre()
    assert_equal(genre.string, "Music")
    genre = driver.next_genre()
    assert_equal(genre.string, "News & Politics")
    genre = driver.next_genre()
    assert_equal(genre.string, "Religion & Spirituality")
    genre = driver.next_genre()
    assert_equal(genre.string, "Science & Medicine")
    genre = driver.next_genre()
    assert_equal(genre.string, "Society & Culture")
    genre = driver.next_genre()
    assert_equal(genre.string, "Sports & Recreation")
    genre = driver.next_genre()
    assert_equal(genre.string, "TV & Film")
    genre = driver.next_genre()
    assert_equal(genre.string, "Technology")
    genre = driver.next_genre()
    assert_equal(genre, None)

def test_next_genre_from_middle():
    driver = Driver(test_url3, MockFetcher(fetch_values))
    driver.populate_state()
    genre = driver.next_genre()
    assert_equal(genre.string, "Sports & Recreation")

def test_next_subgenre():
    driver = Driver(test_url, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Arts")
    assert_equal(driver.current_subgenre, None)

    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Design")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Fashion & Beauty")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Food")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Literature")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Performing Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Visual Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre, None)

def test_next_subgenre_music():
    driver = Driver(test_url4, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Music")
    assert_equal(driver.current_subgenre, None)

    subgenre = driver.next_subgenre()
    assert_equal(subgenre, None)

def test_next_subgenre_from_middle():
    driver = Driver(test_url5, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Arts")
    assert_equal(driver.current_subgenre.string, "Food")

    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Literature")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Performing Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre.string, "Visual Arts")
    subgenre = driver.next_subgenre()
    assert_equal(subgenre, None)

def test_next_letter():
    driver = Driver(test_url, MockFetcher(fetch_values))
    driver.populate_state()

    for let in "ABCDEFGHIJKLMNOPQRSTUVWXYZ#":
        assert_equal(driver.next_letter().string, let)
        assert_equal(driver.current_letter.string, let)

    assert_equal(driver.next_letter(), None)
    assert_equal(driver.current_letter, None)
    #Should NOT loop back to "A", because we haven't repopulated
    #the queue.
    assert_equal(driver.next_letter(), None)

def test_next_letter_from_middle():
    driver = Driver(test_url3, MockFetcher(fetch_values))
    driver.populate_state()
    letter = driver.next_letter()
    assert_equal(letter.string, "O")
    assert_equal(driver.current_letter.string, "O")

def test_next_page():
    driver = Driver(test_url2, MockFetcher(fetch_values))
    driver.populate_state()

    assert_equal(driver.next_page().string, "2")
    assert_equal(driver.current_page.string, "2")
    assert_equal(driver.next_page().string, "3")
    assert_equal(driver.current_page.string, "3")

def test_next_page_from_middle():
    driver = Driver(test_url3, MockFetcher(fetch_values))
    driver.populate_state()
    page = driver.next_page()
    assert_equal(page.string, "3")
    assert_equal(driver.current_page.string, "3")

def test_next_url():
    fetcher = MockFetcher(fetch_values)
    driver = Driver(test_url, fetcher, NullOutput())
    driver.populate_state()
    next_url = driver.next_url()
    assert_equal(next_url, test_url2)
    urls = driver.process_page(fetcher.fetch(next_url), next_url)
    next_url = driver.next_url()
    expected_url = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2&letter=A&page=2#page"
    assert_equal(next_url, expected_url)

def test_starting_state():
    driver = Driver(test_url, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Arts")
    assert_equal(driver.current_subgenre, None)
    assert_equal(driver.current_letter, None)
    assert_equal(driver.current_page, None)

    driver = Driver(test_url2, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Arts")
    assert_equal(driver.current_subgenre, None)
    assert_equal(driver.current_letter.string, "A")
    assert_equal(driver.current_page.string, "1")

    driver = Driver(test_url3, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Society & Culture")
    assert_equal(driver.current_subgenre, None)
    assert_equal(driver.current_letter.string, "N")
    assert_equal(driver.current_page.string, "2")

    driver = Driver(test_url4, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Music")
    assert_equal(driver.current_subgenre, None)
    assert_equal(driver.current_letter, None)
    assert_equal(driver.current_page, None)

    driver = Driver(test_url5, MockFetcher(fetch_values))
    driver.populate_state()
    assert_equal(driver.current_genre.string, "Arts")
    assert_equal(driver.current_subgenre.string, "Food")
    assert_equal(driver.current_letter, None)
    assert_equal(driver.current_page, None)

def test_return_urls_not_in_history_real_tags():
    fetcher = MockFetcher(fetch_values)
    driver = Driver(test_url3, fetcher)
    driver.populate_state()

    scraper = Scraper(text_from_file(test_url3_file))
    tags = scraper.get_letter_urls()
    #Using two different scrapers because the tags will come from 
    #two different scrapers in real life
    scraper2 = Scraper(text_from_file(test_url3_file))
    tags2 = scraper2.get_letter_urls()

    driver.history = tags2[0:3]
    new_urls = driver.return_urls_not_in_history(tags)
    assert_equal(new_urls, tags[3:])

def test_return_urls_not_in_history_real_tags_single_element():
    fetcher = MockFetcher(fetch_values)
    driver = Driver(test_url3, fetcher)
    driver.populate_state()

    scraper = Scraper(text_from_file(test_url3_file))
    tags = scraper.get_letter_urls()
    #Using two different scrapers because the tags will come from 
    #two different scrapers in real life
    scraper2 = Scraper(text_from_file(test_url3_file))
    tags2 = scraper2.get_letter_urls()

    driver.history = tags2[0]
    new_urls = driver.return_urls_not_in_history(tags)
    assert_equal(new_urls, tags[1:])

def test_repopulate_queues():
    fetcher = MockFetcher(fetch_values)
    driver = Driver(test_url2, fetcher)
    driver.populate_state()

    #Shouldn't change anything
    before_pages = driver.pages
    before_letters = driver.letters
    before_subgenres = driver.subgenres

    driver.repopulate_queues(fetcher.fetch(test_url2))
    assert_equal(before_pages, driver.pages)
    assert_equal(before_letters, driver.letters)
    assert_equal(before_subgenres, driver.subgenres)

def test_repopulate_queues_pages():

    fetcher = MockFetcher(fetch_values)
    driver = Driver(test_url2, fetcher)
    driver.populate_state()
    
    before_pages = driver.pages

    driver.repopulate_queues(fetcher.fetch(test_url2))
    assert_equal(before_pages, driver.pages)

    #move two pages into history
    driver.history = driver.history + driver.pages[0:2]
    after_pages = driver.pages[2::]

    #wipe driver.pages, so that it will actually refresh
    driver.pages = []
    driver.repopulate_queues(fetcher.fetch(test_url2))
    assert_equal(after_pages, driver.pages)

def test_repopulate_queues_letters():

    fetcher = MockFetcher(fetch_values)
    driver = Driver(test_url2, fetcher)
    driver.populate_state()
    
    before_letters = driver.letters

    driver.repopulate_queues(fetcher.fetch(test_url2))
    assert_equal(before_letters, driver.letters)

    #Add the current url to history, since it would normally be there
    driver.history.append(driver.current_letter)

    #move two letters into history
    driver.history = driver.history + driver.letters[0:2]
    after_letters = driver.letters[2::]

    #wipe driver.letters, so that it will actually refresh
    driver.letters = []
    driver.repopulate_queues(fetcher.fetch(test_url2))
    assert_equal(after_letters, driver.letters)

def test_repopulate_queues_subgenres():

    fetcher = MockFetcher(fetch_values)
    driver = Driver(test_url2, fetcher)
    driver.populate_state()
    
    before_subgenres = driver.subgenres

    driver.repopulate_queues(fetcher.fetch(test_url2))
    assert_equal(before_subgenres, driver.subgenres)

    #move two subgenres into history
    driver.history = driver.history + driver.subgenres[0:2]
    after_subgenres = driver.subgenres[2::]

    #wipe driver.subgenres, so that it will actually refresh
    driver.subgenres = []
    driver.repopulate_queues(fetcher.fetch(test_url2))
    assert_equal(after_subgenres, driver.subgenres)

def test_crawl():
    fetcher = MockSingleResultFetcher(test_url_file)
    driver = Driver(test_url2, fetcher, NullOutput())
    driver.populate_state()
    driver.crawl()

    assert_true(len(driver.history) > 32)

    #Since we're feeding the same page in repeatedly, 
    #it is only fetching urls that are on that page.
    # 16 genres + 6 subgenres + 27 letters
    assert_equal(len(driver.history), 49)
    assert_equal(driver.history[-1].string, "Technology")
