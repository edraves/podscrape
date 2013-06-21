from podscrape.models import Url, Podcast

class FileOutput(object):

    def __init__(self, scrape_filename, lookup_filename):
        self.scrape_filename = scrape_filename
        self.lookup_filename = lookup_filename

    def write_scraped_info(self, source_url, genre, subgenre, letter, page, url_list):
        """
        Writes info from scraper to the objects scrape_filename

        Args: 
            source_url: string containing url this was scraped from
            genre: Url containing current_genre or None
            subgenre: Url containing current_subgenre or None
            letter: Url containing current_letter or None
            page: Url containing current_page or None
            url_list: List of Strings containing iTunes podcast urls
        """
        f = open(self.scrape_filename, 'a')

        if genre:
            gen = genre.string
        else:
            gen = "None"

        if subgenre:
            sub = subgenre.string
        else:
            sub = "None"
        if letter:
            let = letter.string
        else:
            let = "Popular"
        if page:
            page_num = page.string
        else:
            page_num = 0
        page_num = str(page_num)

        output_list = [source_url, gen, sub, let, page_num]
        output_list.extend(url_list)
        line = "\t".join(output_list)
        f.write(line)
        f.write("\n")
        f.close()    
