from bs4 import BeautifulSoup

class Scraper(object):

    def __init__(self, filename):
        self.soup = make_soup_from_file(filename)

    def get_itunes_podcast_urls(self):
        podcast_soup = self.soup.find("div", id="selectedcontent")
        a_list = podcast_soup.find_all("a")
        urls = []
        for tag in a_list:
            urls.append(tag.get('href'))
        return urls

    def get_top_level_genre_urls(self):
        genre_soup = self.soup.find("div", id="genre-nav")
        a_list = genre_soup.find_all("a", class_="top-level-genre")
        urls = []
        for tag in a_list:
            urls.append(tag.get('href'))
        return urls

    def get_subgenre_urls(self):
        genre_soup = self.soup.find("div", id="genre-nav")
        subgenre_soup = genre_soup.find(class_="list top-level-subgenres")
        a_list = subgenre_soup.find_all("a")
        urls = []
        for tag in a_list:
            urls.append(tag.get('href'))
        return urls

    def get_number_of_pages(self):
        page_soup = self.soup.find("ul", class_="list paginate")

        if (page_soup is None):
            return 0
        else:
            # I know this will find the numbers plus the next link
            # But due to an off by one error on the site, there's
            # always one link left on an unlisted page.
            a_list = page_soup.find_all("a")
            return len(a_list)

def make_soup_from_file(filename):
    handle = open(filename)
    text = handle.read()
    handle.close()
    soup = BeautifulSoup(text)
    return soup
