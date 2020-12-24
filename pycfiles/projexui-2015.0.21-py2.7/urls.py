# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/urls.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = ' Defines common and useful methods for manipulating URLS. '
import projex.text, urllib, urlparse
from .text import nativestring as nstr

def build(path, query=None, fragment=''):
    """
    Generates a URL based on the inputted path and given query options and
    fragment.  The query should be a dictionary of terms that will be
    generated into the URL, while the fragment is the anchor point within the
    target path that will be navigated to.  If there are any wildcards within
    the path that are found within the query, they will be inserted into the
    path itself and removed from the query string.
    
    :example    |>>> import skyline.gui
                |>>> skyline.gui.build_url('sky://projects/%(project)s',
                |                          {'project': 'Test', 'asset': 'Bob'})
                |'sky://projects/Test/?asset=Bob'
    
    :param      path        | <str>
                query       | <dict> || None
                fragment    | <str> || None
    
    :return     <str> | url
    """
    url = nstr(path)
    keys = projex.text.findkeys(path)
    if keys:
        if query is None:
            query = {}
        opts = {}
        for key in keys:
            opts[key] = query.pop(key, ('%({})s').format(key))

        url %= opts
    if query:
        if type(query) is dict:
            mapped_query = {}
            for key, value in query.items():
                mapped_query[nstr(key)] = nstr(value)

            query_str = urllib.urlencode(mapped_query)
        else:
            query_str = nstr(query)
        url += '?' + query_str
    if fragment:
        url += '#' + fragment
    return url


def parse(url):
    """
    Parses out the information for this url, returning its components
    expanded out to Python objects.
    
    :param      url | <str>
    
    :return     (<str> path, <dict> query, <str> fragment)
    """
    result = urlparse.urlparse(nstr(url))
    path = result.scheme + '://' + result.netloc
    if result.path:
        path += result.path
    query = {}
    if result.query:
        url_query = urlparse.parse_qs(result.query)
        for key, value in url_query.items():
            if type(value) == list and len(value) == 1:
                value = value[0]
            query[key] = value

    return (path, query, result.fragment)


def register(scheme):
    """
    Registers a new scheme to the urlparser.
    
    :param      schema | <str>
    """
    scheme = nstr(scheme)
    urlparse.uses_fragment.append(scheme)
    urlparse.uses_netloc.append(scheme)
    urlparse.uses_params.append(scheme)
    urlparse.uses_query.append(scheme)
    urlparse.uses_relative.append(scheme)