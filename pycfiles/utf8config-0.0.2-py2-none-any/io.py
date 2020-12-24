# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: utf8config/io.py
# Compiled at: 2017-10-14 20:07:45
from __future__ import unicode_literals
from six import integer_types, string_types

def is_same_instance(l):
    """
    Check whether if items in list is same type or None.
    """
    if len(l) == 0:
        raise ValueError
    i1_class = (None).__class__
    for i in l:
        if i is not None:
            i1_class = i.__class__

    for i in l:
        if isinstance(i, i1_class) or i is None:
            pass
        else:
            return False

    return True


TRUE_MARKUP = set([b'true', b'yes', b'是'])
FALSE_MARKUP = set([b'false', b'no', b'否'])
NONE_MARKUP = set([b'none', b'null', b''])

def load_value(text=b'', allow_space=True):
    """
    Load value from string.

    :param allow_space: if True, then allow all space string such as "  ", "  ",
      "
"
    """
    if allow_space:
        if text != b'' and text.strip() == b'':
            return text
        text = text.strip()
    else:
        text = text.strip()
    try:
        return int(text)
    except:
        pass

    try:
        return float(text)
    except:
        pass

    if text.startswith(b"'") and text.endswith(b"'") and b"','" not in text and b"', '" not in text or text.startswith(b'"') and text.endswith(b'"') and b'","' not in text and b'", "' not in text:
        return text[1:-1]
    else:
        if text.lower() in TRUE_MARKUP:
            return True
        if text.lower() in FALSE_MARKUP:
            return False
        if text.lower() in NONE_MARKUP:
            return None
        if b',' in text:
            if text == b',':
                return list()
            value = [ load_value(s, allow_space=False) for s in text.split(b',') ]
            if is_same_instance(value):
                return value
            raise ValueError(b'items in list has to be same type!')
        return text


def dump_value(value=None, allow_space=True):
    """
    stringlize the value.

    - None -> "None"
    - True -> "True"
    - False -> "False"
    - 1 -> "1"
    - 3.14 -> "3.14"
    - "Hello World" -> "Hello World"
    - "1" -> '"1"'
    - "3.14" -> '"3.14"'
    """
    if value is None:
        return b'None'
    else:
        if value is True:
            return b'True'
        if value is False:
            return b'False'
        if isinstance(value, integer_types):
            return str(value)
        if isinstance(value, float):
            return str(value)
        if isinstance(value, list):
            if not value:
                return b','
            if is_same_instance(value):
                return (b', ').join([ dump_value(v) for v in value ])
            raise ValueError(b'items in list has to be same type!')
        if isinstance(value, string_types):
            if allow_space:
                pass
            else:
                value = value.strip()
            try:
                int(value)
                return b"'%s'" % value
            except:
                pass

            try:
                float(value)
                return b"'%s'" % value
            except:
                pass

            if value.lower() in TRUE_MARKUP | FALSE_MARKUP | NONE_MARKUP:
                return b"'%s'" % value
            return value
        raise ValueError(b"Can't dump %r!" % value)
        return