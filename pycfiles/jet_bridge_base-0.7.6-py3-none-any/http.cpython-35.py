# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/http.py
# Compiled at: 2019-11-08 11:55:37
# Size of source mod 2**32: 786 bytes
import six
from six.moves.urllib import parse

def replace_query_param(url, key, val):
    scheme, netloc, path, query, fragment = parse.urlsplit(six.text_type(url))
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict[six.text_type(key)] = [six.text_type(val)]
    query = parse.urlencode(sorted(list(query_dict.items())), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def remove_query_param(url, key):
    scheme, netloc, path, query, fragment = parse.urlsplit(six.text_type(url))
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict.pop(key, None)
    query = parse.urlencode(sorted(list(query_dict.items())), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))