# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/compat.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2639 bytes
import os
try:
    import simplejson as json
except ImportError:
    import json

try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes

try:
    os.path.expanduser('~')
    expanduser = os.path.expanduser
except (AttributeError, ImportError):
    expanduser = lambda x: x

from boto.vendored import six
from boto.vendored.six import BytesIO, StringIO
from boto.vendored.six.moves import filter, http_client, map, _thread, urllib, zip
from boto.vendored.six.moves.queue import Queue
from boto.vendored.six.moves.urllib.parse import parse_qs, quote, unquote, urlparse, urlsplit
from boto.vendored.six.moves.urllib.request import urlopen
if six.PY3:
    StandardError = Exception
    long_type = int
    from configparser import ConfigParser
else:
    StandardError = StandardError
    long_type = long
    from ConfigParser import SafeConfigParser as ConfigParser