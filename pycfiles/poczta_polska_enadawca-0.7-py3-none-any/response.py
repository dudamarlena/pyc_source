# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/thirdparty/requests/packages/urllib3/util/response.py
# Compiled at: 2018-11-28 03:20:10


def is_fp_closed(obj):
    """
    Checks whether a given file-like object is closed.

    :param obj:
        The file-like object to check.
    """
    try:
        return obj.closed
    except AttributeError:
        pass

    try:
        return obj.fp is None
    except AttributeError:
        pass

    raise ValueError('Unable to determine whether fp is closed.')
    return