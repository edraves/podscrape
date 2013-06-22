from models import Url
import re

class Driver(object):
    """
    Handles the traversal strategy of scraping the Podcast directory.

    Takes a url to begin crawling from, and moves through each Genre,
    Subgenre, Letter, and Page. If the url is from somewhere in the middle
    of its traversal strategy, it does not crawl from the beginning.
    This is so that a failed or aborted crawl can be resumed later.
    """

    def __init__(self, starting_url, fetcher=None, output=None):
        self.start = starting_url
        self.fetcher = fetcher
        self.output = output
        self.history = []

    def populate_state(self):
        """ 
        Fetch starting url; establish starting state of traversal.

        Populate the genre, subgenre, letter, and page queues.
        Store which Tags are currently selected (how far
        into the page we are starting). Remove any Tags that 
        appear 'behind' the starting page.

        """
        scraper = self.fetcher.fetch(self.start)
        self.genres = scraper.get_top_level_genre_urls()
        self.subgenres = scraper.get_subgenre_urls()
        self.letters = scraper.get_letter_urls()
        self.pages = scraper.get_page_urls()

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

        return scraper

    def crawl(self):
        """
        Begin the main crawling loop

        Start by populating the state of the queues, 
        and process the starting_url

        """
        scraper = self.populate_state()
        self.history.append(Url(self.start))
        self.process_page(scraper, self.start)

        while self.genres or self.subgenres or self.letters or self.pages:
            url = self.next_url()
            scraper = self.fetcher.fetch(url)
            self.process_page(scraper, url)

    def next_url(self):
        """
        Returns the URL we should scrape next

        First cycle through pages, then letters, then subgenres, 
        then move to the next genre. Remember that the first page of
        any letter is no page at all, to scrape the popular page.

        """
        tag = None
        if self.pages:
            tag = self.next_page()
        elif self.letters:
            tag = self.next_letter()
        elif self.subgenres:
            tag = self.next_subgenre()
        elif self.genres:
            tag = self.next_genre()
        if tag:
            self.history.append(tag)
        return tag.href

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

    def next_letter(self):
        """Pop next letter from queue, and return it."""
        if (self.letters):
            self.current_letter = self.letters.pop(0)
        else:
            self.current_letter = None
        return self.current_letter

    def next_page(self):
        """Pop next page from queue, and return it."""
        if (self.pages):
            self.current_page = self.pages.pop(0)
        else:
            self.current_page = None
        return self.current_page

    def process_page(self, scraper, source_url):
        """
        Processes page elements and manages output.

        Gets the iTunes urls from the scraper, 
        Writes pertinent info to self.output

        Uses fetcher to do a batch lookup of the iTunes urls.
        Writes those podcast entries to self.output

        Also refills the navigation queues when necessary.
        """
        itunes_urls = scraper.get_itunes_podcast_urls()
        self.output.write_scraped_info(source_url, self.current_genre,
                                       self.current_subgenre,
                                       self.current_letter,
                                       self.current_page, itunes_urls)

        podcasts = self.fetcher.batch_lookup(itunes_urls)
        self.output.write_lookup_info(podcasts)

        self.repopulate_queues(scraper)

    def repopulate_queues(self, scraper):
        """
        Refresh the queues from currently scraped page

        Will only update a queue if it's empty. If it's not,
        we're in the stretch where a refresh would just re-add
        the urls we've already queued or fetched.

        Compare the urls against the history to prevent re-scraping
        """
        if not self.pages:
            page_urls = scraper.get_page_urls()
            self.pages = self.return_urls_not_in_history(page_urls)
        if not self.letters:
            tags = scraper.get_letter_urls()
            self.letters = self.return_urls_not_in_history(tags)
        if not self.subgenres:
            tags = scraper.get_subgenre_urls()
            self.subgenres = self.return_urls_not_in_history(tags)

    def return_urls_not_in_history(self, new_urls):
        """
        Check a list of Tags against the fetch history

        Take a list of Tags, and compare their hrefs
        against self.history. Return any Tags with urls
        that haven't been scraped yet as a list.

        Args: new_urls - A list of Tags

        """
        return_urls = []
        if new_urls:
            for item in new_urls:
                item_already_scraped = False

                if isinstance(self.history, Url):
                    if item.href == self.history.href:
                        item_already_scraped = True

                else:
                    for previous_url in self.history:
                        if item.href == previous_url.href:
                            item_already_scraped = True
                            break

                if not item_already_scraped:
                    return_urls.append(item)

        return return_urls
