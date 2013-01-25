import re
class Driver:

    def __init__(self, starting_url):
        self.start = starting_url
        self.fetcher = None
        self.history = []
        self.current_letter, self.current_page = self.parse_url(starting_url)
#parse out current letter, and page.
#set up genre list, and subgenre list
#first cycle through pages, then letters, then subgenres, then move to the
#next genre.
#Remember that the first page of any letter is no page at all, to scrape the
#popular page.
    def next_page(self):
        #if (self.current_page < self.last_page):
        next_url = self.start
        self.history.append(next_url)
        return next_url

    def parse_url(self, url):
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
