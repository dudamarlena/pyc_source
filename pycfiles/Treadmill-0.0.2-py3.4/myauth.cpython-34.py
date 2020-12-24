# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/plugins/rest/auth/myauth.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 150 bytes
"""
Authentication plugin.
"""

def wrap(wsgi_app, protect):
    """Wrap FLASK app for custom authentication."""
    del protect
    return wsgi_app