# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\srllib\inspect.py
# Compiled at: 2012-05-11 12:09:02
""" Object inspection utilities.
"""

def _getattr_recursive(obj, attr, include_bases):
    try:
        return getattr(obj, attr)
    except AttributeError:
        if include_bases:
            for cls in obj.__bases__:
                try:
                    return _getattr_recursive(cls, attr, include_bases)
                except AttributeError:
                    continue


def get_members(obj, predicate=None, include_bases=True):
    """ Replacement for inspect.getmembers.
    @param predicate: If specified, a function which takes a class attribute and
    indicates (True/False) whether or not it should be included.
    @return: Dictionary of members.
    """
    mems = {}
    for attr in dir(obj):
        val = _getattr_recursive(obj, attr, include_bases)
        if predicate is None or predicate(val):
            mems[attr] = val

    return mems