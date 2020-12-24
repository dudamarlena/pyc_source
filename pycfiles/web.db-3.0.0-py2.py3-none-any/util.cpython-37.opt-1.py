# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/db/util.py
# Compiled at: 2019-06-09 23:34:04
# Size of source mod 2**32: 200 bytes
import re
_safe_uri_replace = re.compile('(\\w+)://(\\w+):(?P<password>[^@]+)@')

def redact_uri(uri, redact=True):
    if '@' in uri:
        if redact:
            return _safe_uri_replace.sub('\\1://\\2@', uri)
    return uri