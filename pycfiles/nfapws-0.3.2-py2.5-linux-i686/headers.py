# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fapws/contrib/headers.py
# Compiled at: 2009-08-20 03:05:56


def redirect(start_response, location, permanent=None):
    header = [('location', location),
     ('Content-Type', 'text/plain')]
    if permanent:
        start_response('301 Moved Permanently', header)
    else:
        start_response('302 Moved Temporarily', header)
    return []