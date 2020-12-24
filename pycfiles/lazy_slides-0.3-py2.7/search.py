# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/search.py
# Compiled at: 2012-01-02 14:05:57
import logging
from . import flickr
log = logging.getLogger(__name__)
search_function = None

def search(tag):
    """Search for an image file matching a given tag using the
    configured search function.

    This uses `search_function` to do the actual search, so make sure
    it's set before you use this.

    :param tag: The tag to search on.
    :raise ValueError: The search function is not set.
    :raise KeyError: No match is found for `tag`.
    :return: A URL.
    """
    log.info(('search function: {}.{}').format(search_function.__module__, search_function.__name__))
    if search_function is None:
        raise ValueError('You need to set lazy_slides.search.search_function before using search_photos()!')
    log.info(('searching for images tagged with "{}"').format(tag))
    url = search_function(tag=tag)
    if url is None:
        raise KeyError(('No results for "{}"').format(tag))
    log.info(('found photo: {}').format(url))
    return url