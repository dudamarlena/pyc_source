# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/compat.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = "pyramid_fullauth's compatibility file for python2 and 3."
import sys
if sys.version_info.major == 2:
    from urllib import urlencode
    from urlparse import urlparse, parse_qs
    from hashlib import algorithms
else:
    from urllib.parse import urlencode, urlparse, parse_qs
    from hashlib import algorithms_guaranteed as algorithms
__all__ = ('urlencode', 'urlparse', 'parse_qs', 'algorithms')