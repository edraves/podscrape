#!/usr/bin/python

"""
Example script for how to run the crawler
"""

from podscrape.driver import Driver
from podscrape.fetcher import Fetcher
from podscrape.output import FileOutput

# The url to start scraping from. This is one near the end
# according to Podscrape's strategy.
# the first url would be: "https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2"
starting_url = "https://itunes.apple.com/us/genre/podcasts-technology-tech-news/id1448?mt=2&letter=T"

# Instantiate a Fetcher so we can make http requests
fetcher = Fetcher()

# Prepare File Output
scraped_info_file = "./scraped_info.csv"
lookup_info_file = "./lookup_info.csv"
output = FileOutput(scraped_info_file, lookup_info_file)

# Initialize the Driver object
driver = Driver(starting_url, fetcher, output)

# Start crawling!
driver.crawl()
