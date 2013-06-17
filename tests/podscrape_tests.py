from podscrape.scraper import Scraper
from nose.tools import *

first_page_filename = "./tests/testcases/itunes_arts_page.html"
page_num_filename = "./tests/testcases/itunes_arts_page_letter_a.html"
music_page_filename = "./tests/testcases/itunes_music_page.html"
food_page_filename = "./tests/testcases/itunes_arts_food_page.html"
society_n2_filename = "./tests/testcases/itunes_society_and_culture_n_2.html"

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

def test_get_top_level_genre_tags():
    scraper = Scraper(first_page_filename)
    genre_urls = scraper.get_top_level_genre_tags()

    assert_equal(len(genre_urls), 16)
    assert_equal(genre_urls[0].string, "Arts")
    assert_equal(genre_urls[1].string, "Business")

def test_get_subgenre_urls():
    scraper = Scraper(first_page_filename)
    subgenre_urls = scraper.get_subgenre_urls()

    assert_equal(len(subgenre_urls), 6)
    assert_equal(subgenre_urls[0], "https://itunes.apple.com/us/genre/podcasts-arts-design/id1402?mt=2")

def test_get_subgenre_urls_no_entries():
    scraper = Scraper(music_page_filename)
    subgenre_urls = scraper.get_subgenre_urls()

    assert_equal(subgenre_urls, None)

def test_get_subgenre_tags():
    scraper = Scraper(first_page_filename)
    subgenre_tags = scraper.get_subgenre_tags()

    assert_equal(len(subgenre_tags), 6)
    assert_equal(subgenre_tags[0].string, "Design")
    assert_equal(subgenre_tags[1].string, "Fashion & Beauty")

def test_get_subgenre_tags_no_entries():
    scraper = Scraper(music_page_filename)
    subgenre_tags = scraper.get_subgenre_tags()

    assert_equal(subgenre_tags, None)

def test_get_number_of_pages():
    scraper = Scraper(page_num_filename)
    num_pages = scraper.get_number_of_pages()
    assert_equal(num_pages, 7)

    scraper = Scraper(first_page_filename)
    num_pages = scraper.get_number_of_pages()
    assert_equal(num_pages, 0)

def test_get_letter_tags():
    scraper = Scraper(first_page_filename)
    letter_tags = scraper.get_letter_tags()
    assert_equal(letter_tags[0].string, "A")
    assert_equal(letter_tags[-1].string, "#")

def test_get_page_tags():
    scraper = Scraper(page_num_filename)
    page_tags = scraper.get_page_tags()
    assert_equal(page_tags[0].string, "2")
    assert_equal(page_tags[-1].string, "7")

def test_get_current_subgenre():
    #Test a page that has a subgenre
    scraper = Scraper(food_page_filename)
    current_subgenre = scraper.get_currently_selected_subgenre()
    assert_equal(current_subgenre.string, "Food")

    #Test a page that doesn't have one
    scraper = Scraper(first_page_filename)
    current_subgenre = scraper.get_currently_selected_subgenre()
    assert_equal(current_subgenre, None)

def test_get_current_genre():
    #Test that a page has a genre selected
    scraper = Scraper(first_page_filename)
    current_genre = scraper.get_currently_selected_genre()
    assert_equal(current_genre.string, "Arts")

    #Test that a page that isn't the base page
    scraper = Scraper(music_page_filename)
    current_genre = scraper.get_currently_selected_genre()
    assert_equal(current_genre.string, "Music")

    #Test a page that has a subgenre selected
    scraper = Scraper(food_page_filename)
    current_genre = scraper.get_currently_selected_genre()
    assert_equal(current_genre.string, "Arts")

def test_get_current_letter():
    #Test a page with a letter selected
    scraper = Scraper(page_num_filename)
    current_letter = scraper.get_currently_selected_letter()
    assert_equal(current_letter.string, "A")

    #Test a page with a letter other than "A"
    scraper = Scraper(society_n2_filename)
    current_letter = scraper.get_currently_selected_letter()
    assert_equal(current_letter.string, "N")

    #Test a page without a letter selected
    scraper = Scraper(first_page_filename)
    current_letter = scraper.get_currently_selected_letter()
    assert_equal(current_letter, None)
