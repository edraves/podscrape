import re
class Driver:

    def __init__(self, starting_url, fetcher=None):
        self.start = starting_url
        self.fetcher = fetcher
        self.history = []
        self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#"
        self.unicode_alpha = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ#"
        self.current_letter, self.current_page = parse_url(starting_url)
        self.populate_state()

#set up genre list, and subgenre list
    def populate_state(self):
        scraper = self.fetcher.fetch(self.start)
        self.genres = scraper.get_top_level_genre_tags()
        self.subgenres = scraper.get_subgenre_tags()
        self.letters = scraper.get_letter_tags()
        self.pages = scraper.get_page_tags()

#        if self.letters:
#            if self.current_letter:
#                print "have letters, and current_letter"
#                for idx, tag in enumerate(self.letters):
#                    if tag['href'].find(unicode(self.start)) >= 0:
#                        print "Url is in letters, index: %r" % idx
#                        self.letters[0:idx] = []

#            elif self.pages:
#                print "pages exists"
#                print "self.start: %r" % self.start
#                for idx, tag in enumerate(self.pages):
#                    print "href: %r" % tag['href']
#                    if tag['href'].find(unicode(self.start)) >= 0:
#                        print "Url is in pages, index: ", idx
#                        self.pages[0:idx] = []
#                        letter_index = self.unicode_alpha.find(self.current_letter)
#                        print "letter index: %r" % letter_index
#                        self.letters[0:letter_index] = []

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
    def next_url(self):
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
                index = self.alpha.find(self.current_letter)
                self.current_letter = self.alpha[index + 1]
                return self.current_letter
        else:
            self.current_letter = self.alpha[0]
            return self.current_letter

    def process_page(self, scraper):
        if not self.pages:
            self.pages = scraper.get_page_tags()
        if not self.letters:
            self.letters = scraper.get_letter_tags()
        if not self.subgenres:
            self.subgenres = scraper.get_subgenre_tags()

        return scraper.get_itunes_podcast_urls()

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
