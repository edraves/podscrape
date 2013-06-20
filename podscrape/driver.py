from bs4 import Tag
import re

class Driver:
    """
    Handles the traversal strategy of scraping the Podcast directory.

    Takes a url to begin crawling from, and moves through each Genre,
    Subgenre, Letter, and Page. If the url is from somewhere in the middle
    of its traversal strategy, it does not crawl from the beginning.
    This is so that a failed or aborted crawl can be resumed later.
    """

    def __init__(self, starting_url, fetcher=None):
        self.start = starting_url
        self.fetcher = fetcher
        self.history = []
        self.populate_state()

    def populate_state(self):
        """ 
        Fetch starting url; establish starting state of traversal.

        Populate the genre, subgenre, letter, and page queues.
        Store which Tags are currently selected (how far
        into the page we are starting). Remove any Tags that 
        appear 'behind' the starting page.

        """
        scraper = self.fetcher.fetch(self.start)
        self.genres = scraper.get_top_level_genre_tags()
        self.subgenres = scraper.get_subgenre_tags()
        self.letters = scraper.get_letter_tags()
        self.pages = scraper.get_page_tags()

        #Collect each of the current selected Tags
        self.current_subgenre = scraper.get_currently_selected_subgenre()
        self.current_genre = scraper.get_currently_selected_genre()
        self.current_letter = scraper.get_currently_selected_letter()
        self.current_page = scraper.get_currently_selected_page()

        # We want to slice out the preceding genres, so we start in the
        # right place. Add one to remove the current genre from the list.
        # If currently selected is a subgenre, remove all prior 
        # top level genres
        current_index = self.genres.index(self.current_genre) + 1
        self.genres[0:current_index] = []

        if self.current_subgenre:
            current_index = self.subgenres.index(self.current_subgenre) + 1
            self.subgenres[0:current_index] = []

        if self.current_letter:
            current_index = self.letters.index(self.current_letter) + 1
            self.letters[0:current_index] = []

        if self.current_page:
            if self.current_page in self.pages:
                current_index = self.pages.index(self.current_page) + 1
                self.pages[0:current_index] = []

    def next_url(self):
        """
        Returns the URL we should scrape next

        First cycle through pages, then letters, then subgenres, 
        then move to the next genre. Remember that the first page of
        any letter is no page at all, to scrape the popular page.

        """
        tag = None
        if self.pages:
            tag = self.pages.pop(0)
        elif self.letters:
            tag = self.letters.pop(0)
        elif self.subgenres:
            tag = self.next_subgenre()
        elif self.genres:
            tag = self.next_genre()
        if tag:
            self.history.append(tag)
        return tag['href']

    def next_genre(self):
        """Pop next genre from queue, and return it."""
        if (self.genres):
            self.current_genre = self.genres.pop(0)
        else:
            self.current_genre = None
        return self.current_genre

    def next_subgenre(self):
        """Pop next subgenre from queue, and return it."""
        if (self.subgenres):
            self.current_subgenre = self.subgenres.pop(0)
        else:
            self.current_subgenre = None
        return self.current_subgenre

    def process_page(self, scraper):
        """
        Returns the podcast urls contained by a scraper.

        Also refills the navigation queues when necessary.
        """
        #TODO Test and hook in return_urls_not_in_history()
        if not self.pages:
            self.pages = scraper.get_page_tags()
        if not self.letters:
            self.letters = scraper.get_letter_tags()
        if not self.subgenres:
            self.subgenres = scraper.get_subgenre_tags()

        return scraper.get_itunes_podcast_urls()

    def return_urls_not_in_history(self, new_urls):
        """
        Check a list of Tags against the fetch history

        Take a list of Tags, and compare their hrefs
        against self.history. Return any Tags with urls
        that haven't been scraped yet as a list.

        Args: new_urls - A list of Tags

        """
        return_urls = []
        for item in new_urls:
             item_already_scraped = False

             if isinstance(self.history, Tag):
                 if item['href'] == self.history['href']:
                     item_already_scraped = True

             else:
                 for previous_url in self.history:
                     print "item: %r", (item)
                     print "previous: %r", (previous_url)
                     if item['href'] == previous_url['href']:
                         item_already_scraped = True
                         break

             if not item_already_scraped:
                 return_urls.append(item)

        if len(return_urls) == 0:
            return_urls = None

        return return_urls

    def write_urls_to_file(self, source_url, genre, subgenre, url_list):
        f = open(self.output_file, 'a')
        letter, page = parse_url(source_url)
        if not subgenre:
            subgenre = "none"
        if not letter:
            letter = "Popular"
        page = str(page)
        output_list = [source_url, genre, subgenre, letter, page]
        output_list.extend(url_list)
        line = "\t".join(output_list)
        f.write(line)
        f.write("\n")
        f.close()        

def parse_url(url):
    """Return selected letter and page of a given query string."""
    letter = None
    page = 0
    match = re.search(r"http.*\?.*letter=([A-Z#])", url)
    if match:
        letter = match.group(1)
        page = 1
    match_page = re.search(r"http.*\?.*page=(\d+)", url)
    if match_page:
        page = int(match_page.group(1))
    return letter, page
