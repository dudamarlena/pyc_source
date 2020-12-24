# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/gravatar.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import unicode_literals
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

import format, hashlib

def get_url(email, size=20):
    md5hash = hashlib.md5(email.encode(b'utf-8').lower().strip()).hexdigest()
    base_url = b'https://www.gravatar.com/avatar/' + md5hash
    params = None
    if format.get_selected() == b'html':
        params = {b'default': b'identicon', b'size': size}
    elif format.get_selected() == b'xml':
        params = {b'default': b'identicon'}
    return base_url + b'?' + urlencode(params)