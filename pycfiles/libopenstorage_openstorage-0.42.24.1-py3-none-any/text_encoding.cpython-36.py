# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/text_encoding.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 4855 bytes
"""Encoding related utilities."""
import re, six
_cescape_chr_to_symbol_map = {}
_cescape_chr_to_symbol_map[9] = '\\t'
_cescape_chr_to_symbol_map[10] = '\\n'
_cescape_chr_to_symbol_map[13] = '\\r'
_cescape_chr_to_symbol_map[34] = '\\"'
_cescape_chr_to_symbol_map[39] = "\\'"
_cescape_chr_to_symbol_map[92] = '\\\\'
_cescape_unicode_to_str = [chr(i) for i in range(0, 256)]
for byte, string in _cescape_chr_to_symbol_map.items():
    _cescape_unicode_to_str[byte] = string

_cescape_byte_to_str = ['\\%03o' % i for i in range(0, 32)] + [chr(i) for i in range(32, 127)] + ['\\%03o' % i for i in range(127, 256)]
for byte, string in _cescape_chr_to_symbol_map.items():
    _cescape_byte_to_str[byte] = string

del byte
del string

def CEscape(text, as_utf8):
    """Escape a bytes string for use in an text protocol buffer.

  Args:
    text: A byte string to be escaped.
    as_utf8: Specifies if result may contain non-ASCII characters.
        In Python 3 this allows unescaped non-ASCII Unicode characters.
        In Python 2 the return value will be valid UTF-8 rather than only ASCII.
  Returns:
    Escaped string (str).
  """
    if six.PY3:
        text_is_unicode = isinstance(text, str)
        if as_utf8:
            if text_is_unicode:
                return text.translate(_cescape_chr_to_symbol_map)
        ord_ = ord if text_is_unicode else (lambda x: x)
    else:
        ord_ = ord
    if as_utf8:
        return ''.join(_cescape_unicode_to_str[ord_(c)] for c in text)
    else:
        return ''.join(_cescape_byte_to_str[ord_(c)] for c in text)


_CUNESCAPE_HEX = re.compile('(\\\\+)x([0-9a-fA-F])(?![0-9a-fA-F])')

def CUnescape(text):
    """Unescape a text string with C-style escape sequences to UTF-8 bytes.

  Args:
    text: The data to parse in a str.
  Returns:
    A byte string.
  """

    def ReplaceHex(m):
        if len(m.group(1)) & 1:
            return m.group(1) + 'x0' + m.group(2)
        else:
            return m.group(0)

    result = _CUNESCAPE_HEX.sub(ReplaceHex, text)
    if six.PY2:
        return result.decode('string_escape')
    else:
        return result.encode('utf-8').decode('unicode_escape').encode('raw_unicode_escape')