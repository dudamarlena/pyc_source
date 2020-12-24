# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/utils.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 2123 bytes
import collections, six, os, json
from scrapy.utils import project
from scrapy.http import HtmlResponse
from six.moves.urllib_parse import urlparse

class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def is_sequence(seq):
    """Returns a true if its input is a collections.Sequence (except strings).
    Args:
      seq: an input sequence.
    Returns:
      True if the sequence is a not a string and is a collections.Sequence.
    """
    return isinstance(seq, collections.Sequence) and not isinstance(seq, six.string_types)


def is_string_like(s):
    return isinstance(s, six.string_types) or isinstance(s, six.binary_type) or isinstance(s, bytearray)


def is_string(s):
    return isinstance(s, six.string_types)


def closest_parser_engine_json(fn='parser_engine.json', path='.', prevpath=None):
    """Return the path to the closest parser_engine.json file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    else:
        path = os.path.abspath(path)
        cfgfile = os.path.join(path, fn)
        if os.path.exists(cfgfile):
            return cfgfile
        return closest_parser_engine_json(fn, os.path.dirname(path), path)


def load_scrapy_settings():
    return project.get_project_settings()


def is_not_empty_list(seq):
    return is_sequence(seq) and len(seq) > 0


def is_html_response(response):
    return isinstance(response, HtmlResponse) and b'text/plain' not in response.headers.get(b'Content-Type', b'') and not is_json(response.body)


def is_json_response(response):
    return is_json(response.body)


def is_json(s):
    try:
        json.loads(s)
        return True
    except ValueError:
        return False


def item2dict(item):
    return item.__dict__['_values']


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False