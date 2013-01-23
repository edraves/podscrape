from bs4 import BeautifulSoup

class Scraper(object):

    def __init__(self, filename):
        self.soup = make_soup_from_file(filename)

    def get_itunes_podcast_urls(self):
        podcast_soup = self.soup.find("div", id="selectedcontent")
        a_list = podcast_soup.find_all("a")
        return a_list

def make_soup_from_file(filename):
    handle = open(filename)
    text = handle.read()
    handle.close()
    soup = BeautifulSoup(text)
    return soup
