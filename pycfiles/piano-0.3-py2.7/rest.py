# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\lib\rest.py
# Compiled at: 2012-03-20 09:36:41
"""
:mod:`piano.libs.rest`
----------------------

.. autofunction:: invoke

"""
import urllib2, simplejson as json

def invoke(url):
    """Invokes a RESTful URL and converts the response to a Python dict().
    """
    data = None
    try:
        try:
            data = urllib2.urlopen(url).read()
        except urllib2.HTTPError as e:
            print 'HTTP error: %d' % e.code
        except urllib2.URLError as e:
            print 'Network error: %s' % e.reason.args[1]

    finally:
        if data is not None:
            return json.loads(data)

    return