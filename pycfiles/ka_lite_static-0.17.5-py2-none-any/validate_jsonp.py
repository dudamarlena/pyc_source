# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/utils/validate_jsonp.py
# Compiled at: 2018-07-11 18:15:32
"""Validate Javascript Identifiers for use as JSON-P callback parameters."""
from __future__ import unicode_literals
import re
from unicodedata import category
from django.utils import six
valid_jsid_categories_start = frozenset([
 b'Lu', b'Ll', b'Lt', b'Lm', b'Lo', b'Nl'])
valid_jsid_categories = frozenset([
 b'Lu', b'Ll', b'Lt', b'Lm', b'Lo', b'Nl', b'Mn', b'Mc', b'Nd', b'Pc'])
valid_jsid_chars = ('$', '_')
array_index_regex = re.compile(b'\\[[0-9]+\\]$')
has_valid_array_index = array_index_regex.search
replace_array_index = array_index_regex.sub
is_reserved_js_word = frozenset([
 b'abstract', b'boolean', b'break', b'byte', b'case', b'catch', b'char', b'class',
 b'const', b'continue', b'debugger', b'default', b'delete', b'do', b'double',
 b'else', b'enum', b'export', b'extends', b'false', b'final', b'finally', b'float',
 b'for', b'function', b'goto', b'if', b'implements', b'import', b'in',
 b'instanceof', b'int', b'interface', b'long', b'native', b'new', b'null',
 b'package', b'private', b'protected', b'public', b'return', b'short', b'static',
 b'super', b'switch', b'synchronized', b'this', b'throw', b'throws', b'transient',
 b'true', b'try', b'typeof', b'var', b'void', b'volatile', b'while', b'with']).__contains__

def is_valid_javascript_identifier(identifier, escape=b'\\\\u', ucd_cat=category):
    """Return whether the given ``id`` is a valid Javascript identifier."""
    if not identifier:
        return False
    if not isinstance(identifier, six.text_type):
        try:
            identifier = six.text_type(identifier, b'utf-8')
        except UnicodeDecodeError:
            return False

    if escape in identifier:
        new = []
        add_char = new.append
        split_id = identifier.split(escape)
        add_char(split_id.pop(0))
        for segment in split_id:
            if len(segment) < 4:
                return False
            try:
                add_char(unichr(int(b'0x' + segment[:4], 16)))
            except Exception:
                return False

            add_char(segment[4:])

        identifier = (b'').join(new)
    if is_reserved_js_word(identifier):
        return False
    first_char = identifier[0]
    if not (first_char in valid_jsid_chars or ucd_cat(first_char) in valid_jsid_categories_start):
        return False
    for char in identifier[1:]:
        if not (char in valid_jsid_chars or ucd_cat(char) in valid_jsid_categories):
            return False

    return True


def is_valid_jsonp_callback_value(value):
    """Return whether the given ``value`` can be used as a JSON-P callback."""
    for identifier in value.split(b'.'):
        while b'[' in identifier:
            if not has_valid_array_index(identifier):
                return False
            identifier = replace_array_index(b'', identifier)

        if not is_valid_javascript_identifier(identifier):
            return False

    return True


def test():
    u"""
    The function ``is_valid_javascript_identifier`` validates a given
    identifier according to the latest draft of the ECMAScript 5 Specification:

      >>> is_valid_javascript_identifier('hello')
      True

      >>> is_valid_javascript_identifier('alert()')
      False

      >>> is_valid_javascript_identifier('a-b')
      False

      >>> is_valid_javascript_identifier('23foo')
      False

      >>> is_valid_javascript_identifier('foo23')
      True

      >>> is_valid_javascript_identifier('$210')
      True

      >>> is_valid_javascript_identifier(u'Straße')
      True

      >>> is_valid_javascript_identifier(r'b') # u'b'
      True

      >>> is_valid_javascript_identifier(r' ')
      False

      >>> is_valid_javascript_identifier('_bar')
      True

      >>> is_valid_javascript_identifier('some_var')
      True

      >>> is_valid_javascript_identifier('$')
      True

    But ``is_valid_jsonp_callback_value`` is the function you want to use for
    validating JSON-P callback parameter values:

      >>> is_valid_jsonp_callback_value('somevar')
      True

      >>> is_valid_jsonp_callback_value('function')
      False

      >>> is_valid_jsonp_callback_value(' somevar')
      False

    It supports the possibility of '.' being present in the callback name, e.g.

      >>> is_valid_jsonp_callback_value('$.ajaxHandler')
      True

      >>> is_valid_jsonp_callback_value('$.23')
      False

    As well as the pattern of providing an array index lookup, e.g.

      >>> is_valid_jsonp_callback_value('array_of_functions[42]')
      True

      >>> is_valid_jsonp_callback_value('array_of_functions[42][1]')
      True

      >>> is_valid_jsonp_callback_value('$.ajaxHandler[42][1].foo')
      True

      >>> is_valid_jsonp_callback_value('array_of_functions[42]foo[1]')
      False

      >>> is_valid_jsonp_callback_value('array_of_functions[]')
      False

      >>> is_valid_jsonp_callback_value('array_of_functions["key"]')
      False

    Enjoy!

    """
    pass


if __name__ == b'__main__':
    import doctest
    doctest.testmod()