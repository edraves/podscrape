import re
class Driver:

    def __init__(self, starting_url, fetcher=None):
        self.start = starting_url
        self.fetcher = fetcher
        self.history = []
        self.current_letter, self.current_page = parse_url(starting_url)
        self.populate_state()

#set up genre list, and subgenre list
    def populate_state(self):
        scraper = self.fetcher.fetch(self.start)
        self.genres = scraper.get_top_level_genre_tags()

        #Loop through to see which tag has selected in the class
        for tag in self.genres:
            if "selected" in tag['class']:
                self.current_genre = tag
                break

        #We want to slice out the preceding genres, so we start in the
        #right place. Add one to remove the current genre from the list
        current_index = self.genres.index(self.current_genre) + 1
        self.genres[0:current_index] = []
#first cycle through pages, then letters, then subgenres, then move to the
#next genre.
#Remember that the first page of any letter is no page at all, to scrape the
#popular page.
#    def next_page(self):
#        #if (self.current_page < self.last_page):
#        next_url = self.start
#        self.history.append(next_url)
#        return next_url

    def next_genre(self):
        if (self.genres):
            self.current_genre = self.genres.pop(0)
        else:
            self.current_genre = None
        return self.current_genre

#parse out current letter, and page.
def parse_url(url):
    letter = ''
    page = 0
    match = re.search(r"http.*\?.*letter=([A-Z#])", url)
    if match:
        letter = match.group(1)
        page = 1
    match_page = re.search(r"http.*\?.*page=(\d+)", url)
    if match_page:
        page = int(match_page.group(1))
    return letter, page
