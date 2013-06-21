=========
Podscrape
=========

A Python module for crawling the iTunes Podcast_ directory. 

.. _Podcast: https://itunes.apple.com/us/genre/podcasts-arts/id1301?mt=2

The reason for scraping the web pages is to collect each of the podcast urls, which contains the podcast's id number. This id number can be used in Apple's `Lookup API`_ in order to get the podcast's *actual* url (Apple doesn't host any of these podcasts, just puts up a fancy landing page for them on iTunes). Since I use Linux, and don't use iTunes, I'd rather have the original feed urls.

.. _`Lookup API`: http://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.html#lookup

A sample script is included in the root directory of the project. It starts from near the end of the list. If you want to run it from the beginning, the very first url is in a comment in the script. Keep Control+C handy, it will probably run for a while if you let it. I haven't tested to see what kind of rate limiting Apple does, or if they have cutoffs. So consider that before running from the beginning.

Running the Unit Tests::

    # Once nose is installed
    $ nosetests

Dependencies:
    - beautifulsoup4: for parsing and extracting content from web pages
    - nose: for testing (though some of the tests are usable with unittest
    - requests: for making http requests

Set up the Python environment
-----------------------------
Install Virtualenv
~~~~~~~~~~~~~~~~~~
Always use a virtualenv when you install Python package requirements. It saves a ton of pain with library versioning issues, and prevents clutter in the system wide package directory. It also lets you install Python packages through its own internal pip, which doesn't require superuser permissions.

If pip isn't installed, nor available in the package manager repositories, then install distribute first. I use distribute instead of setup-tools because distribute is more forward compatible with Python 3.

Install Distribute::

    $ curl -O http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py

Install Pip::

    $ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    $ [sudo] python get-pip.py

Install Virtualenv::

    $ [sudo] pip install virtualenv

Set up the Virtualenv
~~~~~~~~~~~~~~~~~~~~~
Make a virtualenv for us to run in::

    #This can go wherever. e.g. /usr/local/
    #Creates a new folder './podscrape-env' to hold the environment
    #If you're using setup-tools instead of distribute, leave out the --distribute flag
    $ cd /usr/local
    $ virtualenv podscrape-env --distribute --no-site-packages

Activate the virtualenv::

    $ source /usr/local/podscrape-env/bin/activate

Install the requirements from the project::

    $ cd /path/to/the/code
    $ pip install -r requirements.txt

