# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\compat.py
# Compiled at: 2018-05-16 08:19:14
# Size of source mod 2**32: 686 bytes
import sys
_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3
try:
    import simplejson as json
except ImportError:
    import json
    JSONDecodeError = None
else:
    JSONDecodeError = json.errors.JSONDecodeError
if is_py2:
    if JSONDecodeError is None:
        JSONDecodeError = ValueError
    range = xrange
    unicode = unicode
    from urllib import quote as url_quote
else:
    if is_py3:
        if JSONDecodeError is None:
            JSONDecodeError = json.decoder.JSONDecodeError
        range = range
        unicode = str
        from urllib.parse import quote as url_quote
from requests.compat import bytes, str, basestring