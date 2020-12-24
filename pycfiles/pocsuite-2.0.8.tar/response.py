# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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