# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/utils/urlfetcher.py
# Compiled at: 2012-06-19 10:10:38
"""NDG XACML data fetch by URL utility

NERC DataGrid
"""
__author__ = 'R B Wilkinson'
__date__ = '03/11/11'
__copyright__ = '(C) 2011 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: urlfetcher.py 8078 2012-06-19 14:10:35Z pjkersha $'
import logging, os, urllib2, urlparse
log = logging.getLogger(__name__)

def fetch_stream_from_url(url, debug=False):
    """Returns data retrieved from a URL.
    @param url: URL to attempt to open
    @type: str
    @param debug: debug flag for urllib2
    @type: bool
    @return: data retrieved from URL or None
    @rtype: file derived type
    """
    response = open_url(url, debug)
    return response


def fetch_data_from_url(url, debug=False):
    """Returns data retrieved from a URL.
    @param url: URL to attempt to open
    @type: str
    @param debug: debug flag for urllib2
    @type: bool
    @return: data retrieved from URL or None
    @rtype: str
    """
    response = open_url(url, debug)
    return_data = response.read()
    response.close()
    return return_data


def open_url(url, debug=False):
    """Attempts to open a connection to a specified URL.
    @param url: URL to attempt to open
    @type: str
    @param debug: debug flag for urllib2
    @type: bool
    @return: tuple (
    @rtype: tuple (
        int: returned HTTP status code or 0 if an error occurred
        str: returned message or error description
        file-like: response object
    )
    """
    debuglevel = 1 if debug else 0
    http_handler = urllib2.HTTPHandler(debuglevel=debuglevel)
    handlers = [
     http_handler]
    if not _should_use_proxy(url):
        handlers.append(urllib2.ProxyHandler({}))
        log.debug('Not using proxy')
    opener = urllib2.build_opener(*handlers)
    try:
        response = opener.open(url)
    except urllib2.HTTPError as exc:
        raise Exception(exc.__str__())

    return response


def _should_use_proxy(url):
    """Determines whether a proxy should be used to open a connection to the
    specified URL, based on the value of the no_proxy environment variable.
    @param url: URL
    @type: str
    @return: flag indicating whether proxy should be used
    @rtype: bool
    """
    no_proxy = os.environ.get('no_proxy', '')
    urlObj = urlparse.urlparse(url)
    for np in [ h.strip() for h in no_proxy.split(',') ]:
        if urlObj.hostname == np:
            return False

    return True