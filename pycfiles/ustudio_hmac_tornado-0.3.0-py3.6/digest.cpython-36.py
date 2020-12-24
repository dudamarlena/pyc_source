# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hmacauth/digest.py
# Compiled at: 2017-07-26 11:26:21
# Size of source mod 2**32: 650 bytes
import hmac, hashlib
try:
    from urllib.parse import parse_qs, quote
except ImportError:
    from urlparse import parse_qs
    from urllib import quote

def generate_digest(secret, method, path, query, body):
    parsed_query = parse_qs(query, keep_blank_values=True)
    canonical_query = []
    for key in sorted(parsed_query.keys()):
        for value in sorted(parsed_query[key]):
            canonical_query.append('='.join((key, quote(value))))

    return hmac.new(secret.encode('utf-8'), '\n'.join((method, path, '&'.join(canonical_query), '')).encode('utf-8') + body, hashlib.sha256).hexdigest()