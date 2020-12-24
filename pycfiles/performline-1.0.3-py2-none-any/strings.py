# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ghetzel/src/github.com/PerformLine/python-performline-client/build/lib.linux-x86_64-2.7/performline/embedded/stdlib/utils/strings.py
# Compiled at: 2018-05-17 16:01:23
"""
String formatting and manipulation functions.
"""
from __future__ import absolute_import
import re, six
WORD_OMIT = '[\\W\\s\\_\\-]+'
WORD_SPLIT = re.compile('(?:([A-Z][^A-Z]*)|' + WORD_OMIT + ')')
CAMEL_STRIP = re.compile(WORD_OMIT)

def camelize(value, upperFirst=False):
    """
    Convert a string into "camelCase" or "PascalCase".

    Args:
        value (str): The string to convert.

        upperFirst (bool, optional): Whether to produce "camelCase" or
            "PascalCase" (first letter capitalized).

    Returns:
        str
    """
    value = WORD_SPLIT.split(value)
    value = [ x for x in value if x is not None and not x.strip() == '' ]
    value = ('').join(x.title() for x in value)
    value = re.sub(WORD_OMIT, '', value)
    if upperFirst:
        return value
    else:
        return value[0].lower() + value[1:]
        return


def underscore(value, joiner='_'):
    """
    Convert a string into "snake_case" (words separated by underscores).

    Args:
        value (str): The string to convert.

        joiner (str, optional): The string to use when joining individual words
            if underscore (_) is not desired.

    Returns:
        str
    """
    value = WORD_SPLIT.split(value)
    value = [ x for x in value if x is not None and not x.strip() == '' ]
    return joiner.join(x.strip().lower() for x in value)


def autotype(value):
    if isinstance(value, basestring):
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        if value.lower() == 'null':
            return None
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

    return value


def u(value):
    try:
        return six.u(value)
    except TypeError:
        return value