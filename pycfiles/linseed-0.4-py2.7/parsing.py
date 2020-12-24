# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/parsing.py
# Compiled at: 2011-05-31 11:44:21


def basic_parse(data):
    """Parse whitespace-delimited data of the form "field-name val1
    val2 val3..."

    For each line in `data` of the form "field val1 val2. . .", the creates an entry in a dict
    of the form::
    
      d[field] = [val1, val2, . . .]

    This returns that dict.

    Args:
      * data: The data to parse

    Returns:
      A dict mapping from field name to lists of values.
    """
    data = [ d.split() for d in data ]
    data = dict([ (d[0], d[1:]) for d in data ])
    return data


def paren_parse(data):
    """Like ``basic_parse()``, but this assumes that the field-name
    ends in a ":".

    This strips off the colon, but otherwise works like ``basic_parse()``.

    Args:
      * data: The data to parse

    Returns:
      A dict mapping from field name to lists of values.
    """
    data = [ d.split(':') for d in data ]
    data = [ (k, v.split()) for k, v in data ]
    return dict(data)