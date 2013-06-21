"""
Module of helper functions for using the Lookup API
"""

import json
import re
from podscrape.models import Podcast

def unwrap_json(json_text):
    """
    Extract first result from Lookup json response

    The Lookup API wraps all searches inside a 
    numbered results object e.g. result 1, result 2.
    Since a search on  podcast ID only returns one result,
    we must remove the useless result counter wrapper.

    If json_text is already unwrapped, returns the original
    text.

    """
    json_dict = json.loads(json_text)
    single_json = json_text
    if (u'results' in json_dict):
        single_result = json_dict[u'results'][0]
        single_json = json.dumps(single_result)
    return single_json

def podcast_from_json(json_text):
    """Return Podcast with info from json_text"""
    text = unwrap_json(json_text)
    json_dict = json.loads(text)
    itunes_id = json_dict[u'collectionId']
    name = json_dict[u'collectionName']
    feed_url = json_dict[u'feedUrl']
    return Podcast(itunes_id, name, feed_url)

def itunes_id_from_url(url):
    """Return id number from itunes podcast url"""
    itunes_id = None
    match = re.search(r"http.*/id(\d+)", url)
    if match:
        itunes_id = match.group(1)
    return itunes_id
