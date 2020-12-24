# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/compat.py
# Compiled at: 2017-02-24 16:57:38
"""pyramid_fullauth's compatibility file for python2 and 3."""
import sys
if sys.version_info.major == 2:
    from urllib import urlencode
    from urlparse import urlparse, parse_qs
    from hashlib import algorithms
else:
    from urllib.parse import urlencode, urlparse, parse_qs
    from hashlib import algorithms_guaranteed as algorithms
__all__ = ('urlencode', 'urlparse', 'parse_qs', 'algorithms')