import re
class Driver:

    def __init__(self, starting_url, fetcher=None):
        self.start = starting_url
        self.fetcher = fetcher
        self.history = []
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#"
        self.current_letter, self.current_page = parse_url(starting_url)
        self.populate_state()

#set up genre list, and subgenre list
    def populate_state(self):
        scraper = self.fetcher.fetch(self.start)
        self.genres = scraper.get_top_level_genre_tags()
        self.subgenres = scraper.get_subgenre_tags()

        #Loop through to see which tag has selected in the class
        self.current_subgenre = self.get_currently_selected_subgenre()
        self.current_genre = self.get_currently_selected_genre()

        #We want to slice out the preceding genres, so we start in the
        #right place. Add one to remove the current genre from the list
        #TODO: If currently selected is a subgenre, remove all prior 
        #top level genres
        current_index = self.genres.index(self.current_genre) + 1
        self.genres[0:current_index] = []

        if self.current_subgenre:
            current_index = self.subgenres.index(self.current_subgenre) + 1
            self.subgenres[0:current_index] = []

    def get_currently_selected_genre(self):
        selected = None
        if self.genres:
            for tag in self.genres:
                if "selected" in tag['class']:
                    selected = tag
                    break
    # If the current genre is a subgenre, we want to continue forward from
    # its parent later
            else:
                subgenre = self.get_currently_selected_subgenre()
                if subgenre:
                    parent_li = subgenre.parent.parent.parent
                    selected = parent_li.find("a", class_="top-level-genre")
        return selected

    def get_currently_selected_subgenre(self):
        selected = None
        if self.subgenres:
            parent_list = self.subgenres[0].parent.parent
            selected = parent_list.find("a", class_="selected")
#            for tag in self.subgenres:
#                if "selected" in tag['class']:
#                    selected = tag
#                    break
        return selected
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

    def next_subgenre(self):
        if (self.subgenres):
            self.current_subgenre = self.subgenres.pop(0)
        else:
            self.current_subgenre = None
        return self.current_subgenre

    def next_letter(self):
        if self.current_letter:
            if self.current_letter is "#":
                self.current_letter = None
            else:
                index = self.letters.find(self.current_letter)
                self.current_letter = self.letters[index + 1]
                return self.current_letter
        else:
            self.current_letter = self.letters[0]
            return self.current_letter
#parse out current letter, and page.
def parse_url(url):
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
