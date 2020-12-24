# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/compat.py
# Compiled at: 2017-11-27 05:07:42
__doc__ = ' Utilities to modify the default views response format.\n\nThis code is used ONLY for compat. It has been imported from\nocs-api@502fafdd9a1e65b1a1b11962 and it SHOULD NOT be modified.\n\nSee ConfView.conf for more details.\n'
import functools, json, pipes
from flask import request

def shell(response):
    """ Flattens the response JSON-dict data as a list of key-value paris.

    Updates the Content-Type header to "text/plain".

    For each key/value of the dictionary:
    - "Simple" elements (strings, bools, integers) are represented as a string
      "KEY=value". pipes.quote is used to handle escaping.
    - Lists are represented as a string "KEY=n" where n is the number of
      elements in the list, then with one line per element "KEY_n=value" where
      n is the index of the element.
    - Dictionaries are represented as a string "KEY=a b c" where a, b, c are
      the keys of the dictionary, then with one line per element "KEY_X=value"
      where X is the dictionary key.

    Example:

    >>> shell({
    ...     'hello': 'world',
    ...     'complex': 'value with spaces',
    ...     'list': ['one', 'two'],
    ...     'dict': {
    ...         'first': 'value',
    ...         'second': 'value with spaces',
    ...         'third': ['x', 'xx', 'xxx']
    ...     }
    ... })
    HELLO=world
    COMPLEX='value with spaces'
    LIST=2
    LIST_0=one
    LIST_1=two
    DICT=FIRST SECOND THIRD
    DICT_FIRST=value
    DICT_SECOND='value with spaces'
    DICT_THIRD=3
    DICT_THIRD_0=x
    DICT_THIRD_1=xx
    DICT_THIRD_2=xxx
    """

    def _transform_line(key, value):
        """ Transforms a single line (simple type, list or dict).
        """

        def make_key(key):
            """ Make key """
            return key.upper()

        if isinstance(value, dict):
            out = '%s=%s\n' % (
             make_key(key), (' ').join(make_key(key) for key in value.keys()))
            for elem_key, elem_value in value.items():
                out += _transform_line(make_key('%s_%s' % (key, elem_key)), elem_value)

            return out
        if isinstance(value, list):
            out = '%s=%s\n' % (make_key(key), len(value))
            for idx, elem in enumerate(value):
                out += _transform_line(make_key('%s_%s' % (key, idx)), elem)

            return out
        value = unicode(value)
        return '%s=%s\n' % (make_key(key), pipes.quote(value))

    response.headers['Content-Type'] = 'text/plain'
    response.data = ('').join(_transform_line(key, value) for key, value in json.loads(response.data).items())
    return response


def select_export(default=None):
    """ Captures the querystring argument "format" to change the response
    output.

    Possible formats:
    - sh (ocs.api.exports.shell)
    - anything else doesn't change the default behaviour.

    :param default: the format used if the querystring argument "format" is not
    provided.
    """

    def decorator(view):

        @functools.wraps(view)
        def wrapped(*args, **kwargs):
            response = view(*args, **kwargs)
            export_type = request.args.get('format')
            if not export_type:
                export_type = default
            exports = {'sh': shell}
            export = exports.get(export_type)
            if export:
                return export(response)
            return response

        return wrapped

    return decorator