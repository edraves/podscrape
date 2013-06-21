from unittest import TestCase
from podscrape.models import Podcast, Url
from podscrape.output import FileOutput

class TestFileOutput(TestCase):

    def test_write_scraped_info(self):
        scrape_filename = "./tests/testcases/scrape.csv"
        lookup_filename = "./tests/testcases/lookups.csv"

        f = open(scrape_filename, 'w')
        f.truncate()
        f.close()
        output = FileOutput(scrape_filename, lookup_filename)

        source_url = "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2"
        genre = Url("https://apple.com/podcast/arts","Arts")
        subgenre = None
        letter = None
        page = None
        urls = []
        for i in range(10):
            urls.append("https://apple.com/podcast/arts/id" + str(i))

        output.write_scraped_info(source_url, genre, subgenre, letter, page, urls)

        f = open(output.scrape_filename)
        text = f.read()
        f.close()
        split_text = text.split("\t")
        self.assertEqual(split_text[0], source_url)
        self.assertEqual(split_text[1], genre.string)
        self.assertEqual(split_text[2], "None")
        self.assertEqual(split_text[3], "Popular")
        self.assertEqual(split_text[4], "0")

        self.assertEqual(split_text[5], urls[0])
        self.assertEqual(split_text[6], urls[1])
        self.assertEqual(split_text[7], urls[2])
        self.assertEqual(split_text[8], urls[3])
        self.assertEqual(split_text[9], urls[4])
        self.assertEqual(split_text[10], urls[5])
        self.assertEqual(split_text[11], urls[6])
        self.assertEqual(split_text[12], urls[7])
        self.assertEqual(split_text[13], urls[8])
        self.assertEqual(split_text[14], urls[9] + '\n')
