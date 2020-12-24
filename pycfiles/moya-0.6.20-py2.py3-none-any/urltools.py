# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/urltools.py
# Compiled at: 2015-11-28 06:52:53
from __future__ import unicode_literals
from __future__ import print_function
from .compat import quote_plus, text_type

def _iter_qs_map(qs_map):
    for k, v in qs_map.items():
        if isinstance(v, list):
            for _v in v:
                yield (
                 text_type(k), text_type(_v))

        else:
            yield (
             text_type(k), text_type(v))


def urlencode(query, _quote_plus=quote_plus, _iter_qs=_iter_qs_map):
    """url encode a mapping of query string values"""
    qs = (b'&').join(((b'{}={}').format(_quote_plus(k), _quote_plus(v)) if text_type(v) else _quote_plus(k)) for k, v in _iter_qs(query))
    return qs