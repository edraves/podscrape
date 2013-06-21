#!/usr/bin/python

"""
Example script for how to run the crawler
"""

from podscrape.driver import Driver
from podscrape.fetcher import Fetcher

# The url to start scraping from. This is one near the end
# according to Podscrape's strategy.
# the first url would be: "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2"
starting_url = "https://itunes.apple.com/us/genre/podcasts-technology/id1318?mt=2&letter=X"

# Instantiate a Fetcher so we can make http requests
fetcher = Fetcher()

# Initialize the Driver object
driver = Driver(starting_url, fetcher)

# Start crawling!
driver.crawl()
