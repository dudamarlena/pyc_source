# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/utils/encoding.py
# Compiled at: 2020-04-14 20:27:46
"""Utilities for managing string types and encoding."""
import six

def force_unicode(string, encoding='utf-8'):
    """Force a given string to be a unicode type.

    Args:
        string (bytes or unicode):
            The string to enforce.

    Returns:
        unicode:
        The string as a unicode type.

    Raises:
        ValueError:
            The given string was not a supported type.
    """
    if isinstance(string, six.text_type):
        return string
    if isinstance(string, bytes):
        return string.decode(encoding)
    raise ValueError('Provided string was neither bytes nor unicode')