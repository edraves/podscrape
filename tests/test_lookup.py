import json
from unittest import TestCase
from podscrape.scraper import Scraper
from podscrape import lookup
from podscrape.models import Podcast

lookup_id = 79687345
lookup_url = "https://itunes.apple.com/us/podcast/npr-all-songs-considered-podcast/id79687345"
lookup_url2 = "https://itunes.apple.com/us/podcast/new-yorker-fiction/id256945396?mt=2"
lookup_json_file = "tests/testcases/curl_result_79687345.json"
single_json_file = "tests/testcases/single_json.json"
feed_url = "http://www.npr.org/rss/podcast.php?id=510019&uid=n1qe4e85742c986fdb81d2d38ffa0d5d53"

class TestLookup(TestCase):

    def test_unwrap_json(self):
        lookup_json = open(lookup_json_file).read()
        single_json = open(single_json_file).read()

        unwrapped = lookup.unwrap_json(lookup_json)
        self.assertEqual(json.loads(unwrapped), json.loads(single_json))

        unwrapped = lookup.unwrap_json(single_json)
        self.assertEqual(unwrapped, single_json)
 
    def test_podcast_from_json(self):
        lookup_json = open(lookup_json_file).read()

        cast = Podcast(lookup_id, "NPR: All Songs Considered Podcast", feed_url)
        json_cast = lookup.podcast_from_json(lookup_json)
        self.assertEqual(cast, json_cast)

    def test_itunes_id_from_url(self):
        itunes_id = lookup.itunes_id_from_url(lookup_url)
        self.assertEqual(lookup_id, itunes_id)

        itunes_id = lookup.itunes_id_from_url(lookup_url2)
        self.assertEqual(256945396, itunes_id)
