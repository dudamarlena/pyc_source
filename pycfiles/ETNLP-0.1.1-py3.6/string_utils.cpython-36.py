# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/utils/string_utils.py
# Compiled at: 2019-03-20 00:39:07
# Size of source mod 2**32: 707 bytes
import six

def convert_to_unicode(text):
    """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
    if six.PY3:
        if isinstance(text, str):
            return text
        if isinstance(text, bytes):
            return text.decode('utf-8', 'ignore')
        raise ValueError('Unsupported string type: %s' % type(text))
    else:
        if six.PY2:
            if isinstance(text, str):
                return text.decode('utf-8', 'ignore')
            if isinstance(text, unicode):
                return text
            raise ValueError('Unsupported string type: %s' % type(text))
        else:
            raise ValueError('Not running on Python2 or Python 3?')