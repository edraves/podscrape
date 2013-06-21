from bs4 import BeautifulSoup
from models import Url

class Scraper(object):
    """
    Extracts elements of an iTunes Podcast directory page.

    Contains the logic to navigate an iTunes Podcast directory page,
    and extract the page elements we are interested in.
    """

    def __init__(self, text):
        self.soup = BeautifulSoup(text)

    def get_itunes_podcast_urls(self):
        """Return a list of all podcast urls on this page."""
        podcast_soup = self.soup.find("div", id="selectedcontent")
        a_list = podcast_soup.find_all("a")
        urls = []
        for tag in a_list:
            urls.append(tag.get('href'))
        return urls

    def get_top_level_genre_tags(self):
        """Return a list of all top level genre tags on this page."""
        genre_soup = self.soup.find("div", id="genre-nav")
        a_list = genre_soup.find_all("a", class_="top-level-genre")
        return a_list

    def get_top_level_genre_urls(self):
        """Return a list of all top level genre urls on this page."""
        a_list = self.get_top_level_genre_tags()
        urls = []
        for tag in a_list:
            new_url = Url(tag.get('href'), tag.string)
            urls.append(new_url)
        return urls

    def get_currently_selected_genre(self):
        """
        Return the Url for the current genre

        If the current genre element with a "selected" css class is a
        subgenre, this will return the subgenre's parent genre.

        """
        selected = None
        genres = self.get_top_level_genre_tags()
        if genres:
            for tag in genres:
                if "selected" in tag['class']:
                    selected = Url(tag.get('href'), tag.string)
                    break
            #No hits in genres means a subgenre is currently selected
            else:
                subgenre = self._get_currently_selected_subgenre_tag()
                if subgenre:
                    parent_li = subgenre.parent.parent.parent
                    selected_tag = parent_li.find("a", class_="top-level-genre")
                    if selected_tag:
                        selected = Url(selected_tag.get('href'), selected_tag.string)
        return selected

    def get_subgenre_tags(self):
        """Return a list of all subgenre tags on this page."""
        genre_soup = self.soup.find("div", id="genre-nav")
        subgenre_soup = genre_soup.find(class_="list top-level-subgenres")
        if subgenre_soup:
            a_list = subgenre_soup.find_all("a")
        else:
            a_list = None
        return a_list

    def get_subgenre_urls(self):
        """Return a list of all subgenre urls on this page."""
        a_list = self.get_subgenre_tags()
        if a_list:
            urls = []
            for tag in a_list:
                new_url = Url(tag.get('href'), tag.string)
                urls.append(new_url)
            return urls
        else:
            return None

    def get_currently_selected_subgenre(self):
        """Return the Url of the currently selected subgenre"""
        selected = None
        selected_tag = self._get_currently_selected_subgenre_tag()
        if selected_tag:
            selected = Url(selected_tag.get('href'), selected_tag.string)
        return selected

    def _get_currently_selected_subgenre_tag(self):
        """Return the Tag of the currently selected subgenre"""
        selected = None
        subgenres = self.get_subgenre_tags()
        if subgenres:
            parent_list = subgenres[0].parent.parent
            selected = parent_list.find("a", class_="selected")
        return selected

    def get_number_of_pages(self):
        """
        Return the number of pages containing podcast links.

        Number returned will be one higher than is visible on the page.
        This is due to an error in Apple's paginator. Apple's
        paginator leaves a single podcast dangling on an unlisted page.

        """
        page_soup = self.soup.find("ul", class_="list paginate")

        if (page_soup is None):
            return 0
        else:
            # I know this will find the numbers plus the next link
            # But due to an off by one error on the site, there's
            # always one link left on an unlisted page.
            a_list = page_soup.find_all("a")
            return len(a_list)

    def get_letter_tags(self):
        """Return a list of all letter tags on this page."""
        letter_soup = self.soup.find("ul", class_="list alpha")
        if letter_soup:
            a_list = letter_soup.find_all("a")
        else:
            a_list = None
        return a_list

    def get_letter_urls(self):
        """Return a list of all letter urls on this page."""
        a_list = self.get_letter_tags()
        if a_list:
            urls = []
            for tag in a_list:
                new_url = Url(tag.get('href'), tag.string)
                urls.append(new_url)
            return urls
        else:
            return None

    def get_currently_selected_letter(self):
        """Return the Url for the current letter"""
        selected = None
        letters = self.get_letter_tags()
        if letters:
            parent_list = letters[0].parent.parent
            selected_tag = parent_list.find("a", class_="selected")
            if selected_tag:
                selected = Url(selected_tag.get('href'), selected_tag.string)
        return selected

    def get_page_tags(self):
        """
        Return a list of all page tags on this page.

        Also adds another incremented tag to the end of the list.
        This is because of a bug in Apple's paginator. Apple's
        paginator leaves a single podcast dangling on an unlisted page.

        """
        page_soup = self.soup.find("ul", class_="list paginate")
        a_list = None
        if page_soup:
            # I know this will find the numbers plus the next link
            # But due to an off by one error on the site, there's
            # always one link left on an unlisted page.
            a_list = page_soup.find_all("a")
            last_href = a_list[-1]['href']
            last_page_number = len(a_list)
            last_page_string = "page=" + str(last_page_number)
            last_href = last_href.replace("page=2", last_page_string)
            a_list[-1]['href'] = last_href
            a_list[-1].string = str(last_page_number)
            a_list.pop(0)
        return a_list

    def get_page_urls(self):
        """Return a list of all page urls on this page."""
        a_list = self.get_page_tags()
        if a_list:
            urls = []
            for tag in a_list:
                new_url = Url(tag.get('href'), tag.string)
                urls.append(new_url)
            return urls
        else:
            return None

    def get_currently_selected_page(self):
        """
        Return the Url for the currently selected page

        Only returns a page if there's something in the paginator

        """
        selected = None
        pages = self.get_page_tags()
        if pages:
            parent_list = pages[0].parent.parent
            selected_tag = parent_list.find("a", class_="selected")
            if selected_tag:
                selected = Url(selected_tag.get('href'), selected_tag.string)
        return selected

def make_soup_from_file(filename):
    """Return BeautifulSoup of the text in filename"""
    handle = open(filename)
    text = handle.read()
    handle.close()
    soup = BeautifulSoup(text)
    return soup
