class Url(object):
    """
    Holds the useful components of a URL
    """

    def __init__(self, href, string=""):
        self.href = href
        self.string = string

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
