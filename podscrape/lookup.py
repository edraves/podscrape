import json

def extract_feed_url(json_text):
    json_dict = json.loads(json_text)
    feed_url = None
    if (u'results' in json_dict):
        single_json = json_dict[u'results'][0]
        if (u'feedUrl' in single_json):
            feed_url = single_json[u'feedUrl']
    elif (u'feedUrl' in json_dict):
        feed_url = json_dict[u'feedUrl']
    return feed_url
