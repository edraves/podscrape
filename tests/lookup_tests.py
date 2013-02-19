import json
from nose.tools import *
from podscrape.scraper import Scraper
from podscrape import lookup

lookup_id = 79687345
lookup_url = "https://itunes.apple.com/us/podcast/npr-all-songs-considered-podcast/id79687345"
lookup_json_file = "tests/testcases/curl_result_79687345.json"
single_json_file = "tests/testcases/single_json.json"
feed_url = "http://www.npr.org/rss/podcast.php?id=510019&uid=n1qe4e85742c986fdb81d2d38ffa0d5d53"

def test_extract_feed_url():
    lookup_json = open(lookup_json_file).read()
    url = lookup.extract_feed_url(lookup_json)
    assert_equal(url, feed_url)

    single_json = open(single_json_file).read()
    url = lookup.extract_feed_url(single_json)
    assert_equal(url, feed_url)
