# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\extractors\extractor.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 7815 bytes
"""This module contains the abstract Extractor class"""
import re, abc
from typing import List, Tuple
from argparse import Namespace
import requests
from bs4 import BeautifulSoup, Tag
import komidl.constants as constants

class Extractor(abc.ABC):
    __doc__ = '\n    Abstract class outlining the core scraping functions for any website module\n    to implement. All abstract public functions must be implemented as they\n    are called by scraper.py\n\n    It is recommended to overwrite these variables in the child classes:\n        self.__PAGE_PATTERN      - General URL pattern for the site, used in\n                                   is_page()\n        self.__GALLERY_PATTERN   - URL pattern for a site gallery, used in\n                                   is_gallery()\n\n    Children may sometimes need to overwrite is_page() and is_gallery().\n    '

    def __init__(self):
        self._PAGE_PATTERN = ''
        self._GALLERY_PATTERN = ''
        self._session = requests.Session()
        self._session.headers = {'User-Agent':constants.USER_AGENT,  'Accept-encoding':'gzip'}
        requests.packages.urllib3.disable_warnings()

    def _get_soup(self, url: str) -> Tag:
        """Returns a BS4 soup from the URL's response.

        This is meant for internal use by classes that implement Extractor.
        """
        request = self._session.get(url, verify=False)
        request.raise_for_status()
        content = request.content
        return BeautifulSoup(content, 'html.parser')

    def get_tests(self) -> Tuple[dict]:
        """Return a tuple of dictionaries representing tests.

        The dictionaries are of the following format:
            {
             "url": "http://extractor-site.com/gallery/blahblah",
             "img_urls": [
                          "http://data.extractor.com/img/blahblah/001.jpg",
                          "http://data.extractor.com/img/blahblah/002.jpg",
                          ...,
                         ],
             "size": 24,
             "tags": {
                      "Title": "Tales of Blah Blah",
                      "Languages": "English",
                      "Artists": "Steve from Minecraft",
                      ...,
                     },
             "series": True,
             "diff_ratio": 0.9,
            }

        For 'img_urls', it is not necessary to list all URLS or the filenames.
        However, the value should at least contain the first few image URLs in
        incrementing order. See below regarding the 'diff_ratio' option.

        Similarly for the 'tags', not all key-value pairs need to exist. The
        values can either be strings or lists of strings since the test suite
        flattens all values for comparison.

        The 'series' key represents if the gallery is for a series (eg. a
        manga with multiple chapters that is ongoing). If the 'series' key
        exists and is set to True, then the tests for size and tags are easier
        to pass. This is because the values are likely to change and the tests
        can easily become out of date. However, the tests will still check for
        basic functionality and extractor function.

        The 'diff_ratio' key modifies the 'img_url' assertion test to be less
        strict. Instead of exact URL matching, the string similarity is found
        with difflib.SequenceMatcher and the ratio must be greater than or
        equal to the given value. This is useful for URLs that may change
        based on access time, but still remain similar.

        See the abstract methods below for further details on proper formats
        for the values.

        Implementation of this method in subclasses is optional.
        """
        pass

    def is_page(self, url: str) -> bool:
        """Return true if the extractor corresponds to the URL's site.

        This is a more generic check compared to is_gallery() as it only checks
        if the URL is for the site the extractor supports (aka. checks the
        hostname).
        """
        return bool(re.match(self._PAGE_PATTERN, url))

    def is_gallery(self, url: str) -> bool:
        """Return true if the extractor can process the URL.

        This is a more precise check compared to is_page(), as it must check
        the URI pattern to see if the URL is a gallery (and thus can be
        scraped).
        """
        return bool(re.match(self._GALLERY_PATTERN, url))

    def reset(self) -> None:
        """Reset the extractor's state.

        Resets may be necessary for subclass implementations that rely on
        private variables to store results of complex calculations or lengthy
        requests. By clearing those variables, it prepares the extractor
        instance for scraping the next URL.

        Implementation of this method in subclasses is optional.
        """
        pass

    @abc.abstractmethod
    def get_size(self, url: str, soup: Tag, args: Namespace) -> int:
        """Return number of images in gallery."""
        pass

    @abc.abstractmethod
    def get_gallery_urls(self, url: str, soup: Tag, args: Namespace) -> List[List[str]]:
        """Return a list of image URLs and the image path to download to."""
        pass

    @abc.abstractmethod
    def get_tags(self, url: str, soup: Tag, args: Namespace) -> dict:
        """Return a dictionary of tags.

        Tags contain information regarding the gallery, such as the title,
        URL, language, artists, etc.

        Keys can be any string, but should at a minimum the dictionary should
        include: ("Title", "Languages", "Artists"/"Authors"/"Groups")

        Values are expected to be either strings, or lists containing strings.

        The following is an example tag dictionary:
        {
            "Title"        : "The Frog Prince",
            "Languages"    : "English",
            "Artists"      : ["Bob Ross", "Picasso"],
            "Groups"       : ["FSF", "Linux Foundation"],
            "Content"      : ["Amphibians", "Fantasy", "Adventure"],
            "URL"          : "http://www.books.com/gallery/the-frog-prince",
        }
        """
        pass