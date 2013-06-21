class Url(object):
    """
    Holds the useful components of a URL
    """

    def __init__(self, href, string=""):
        self.href = href
        self.string = string

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Podcast(object):

    def __init__(self, itunes_id, title, feed_url):
        self.itunes_id = itunes_id
        self.title = title
        self.feed_url = feed_url

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
