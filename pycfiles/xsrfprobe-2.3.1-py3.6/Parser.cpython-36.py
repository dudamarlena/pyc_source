# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Parser.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 2772 bytes
import re
from urllib.parse import urlsplit
from xsrfprobe.core.verbout import verbout
from xsrfprobe.files.dcodelist import PROTOCOLS
from xsrfprobe.files.paramlist import EXCLUSIONS_LIST
from xsrfprobe.core.colors import *

def buildUrl(url, href):
    """
    This function is for building a proper URL based on comparison to 'href'.
    """
    if href == 'http://localhost' or any(re.search(s, href, re.IGNORECASE) for s in EXCLUSIONS_LIST):
        return
    else:
        url_parts = urlsplit(url)
        href_parts = urlsplit(href)
        app = ''
        if href_parts.netloc == url_parts.netloc:
            app = href
        else:
            if len(href_parts.netloc) == 0:
                if len(href_parts.path) != 0 or len(href_parts.query) != 0:
                    domain = url_parts.netloc
                    if href_parts.path.startswith('/'):
                        app = url_parts.scheme + '://' + domain + href_parts.path
                    else:
                        try:
                            app = 'http://' + domain + re.findall(PROTOCOLS, url_parts.path)[0] + href_parts.path
                        except IndexError:
                            app = 'http://' + domain + href_parts.path

                        if href_parts.query:
                            app += '?' + href_parts.query
        return app


def buildAction(url, action):
    """
    The main function of this is to create an action Url based
                on Current Location and Destination.
    """
    verbout(O, 'Parsing URL parameters...')
    if action:
        if not action.startswith('#'):
            return buildUrl(url, action)
    return url