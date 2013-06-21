from unittest import TestCase
from podscrape.models import Url

class UrlTest(TestCase):

    def test_create_url(self):
        href = "http://www.example.com"
        string = "Example"
        url = Url(href)
        self.assertEqual(url.href, href)
        self.assertEqual(url.string, '')

        url = Url(href, string)
        self.assertEqual(url.href, href)
        self.assertEqual(url.string, string)

    def test_url_equality(self):
        href = "http://www.example.com"
        string = "Example"
        url = Url(href, string)
        url2 = Url(href, string)
        self.assertEqual(url, url2)

        url_list = [url]
        self.assertEqual(url_list.index(url2), 0)
