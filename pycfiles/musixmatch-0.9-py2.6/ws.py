# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/musixmatch/ws.py
# Compiled at: 2011-07-29 04:52:54
"""
This is an utility module that provides a row musiXmatch web API interface.
Ideally it should be used like this:

>>> import musixmatch
>>> 
>>> try:
...     chart = musixmatch.ws.track.chart.get(country='it', f_has_lyrics=1)
... except musixmatch.api.Error, e:
...     pass
"""
from warnings import warn
import os, musixmatch.api
__license__ = musixmatch.__license__
__author__ = musixmatch.__author__
_version = os.environ.get('musixmatch_apiversion', None)
if not _version:
    _version = '1.1'
else:
    warn("Use of `musixmatch_apiversion' was deprecated in favour of `musixmatch_wslocation'", DeprecationWarning)
location = os.environ.get('musixmatch_wslocation', 'http://api.musixmatch.com/ws/%s' % _version)
artist = musixmatch.api.Method('artist')
album = musixmatch.api.Method('album')
track = musixmatch.api.Method('track')
tracking = musixmatch.api.Method('tracking')
matcher = musixmatch.api.Method('matcher')