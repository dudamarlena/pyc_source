# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smorin/Dropbox/code/dedup/filegardener/test_data/1dup/seconddir/requests/__init__.py
# Compiled at: 2016-07-21 23:59:52
"""
Requests HTTP library
~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. Basic GET
usage:

   >>> import requests
   >>> r = requests.get('https://www.python.org')
   >>> r.status_code
   200
   >>> 'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = requests.post('http://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key2": "value2",
       "key1": "value1"
     },
     ...
   }

The other HTTP methods are supported - see `requests.api`. Full documentation
is at <http://python-requests.org>.

:copyright: (c) 2016 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.

"""
__title__ = 'requests'
__version__ = '2.10.0'
__build__ = 135168
__author__ = 'Kenneth Reitz'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Kenneth Reitz'
try:
    from .packages.urllib3.contrib import pyopenssl
    pyopenssl.inject_into_urllib3()
except ImportError:
    pass

import warnings
from .packages.urllib3.exceptions import DependencyWarning
warnings.simplefilter('ignore', DependencyWarning)
from . import utils
from .models import Request, Response, PreparedRequest
from .api import request, get, head, post, patch, put, delete, options
from .sessions import session, Session
from .status_codes import codes
from .exceptions import RequestException, Timeout, URLRequired, TooManyRedirects, HTTPError, ConnectionError, FileModeWarning, ConnectTimeout, ReadTimeout
import logging
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
warnings.simplefilter('default', FileModeWarning, append=True)