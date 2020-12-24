# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pgpu/string_utils.py
# Compiled at: 2016-03-15 03:08:23


def print_to_var(*args, **kw):
    """
    Returns strings like those the Python3 print() function writes to file
    objects.
    """
    sep = str(kw.pop('sep', ' '))
    end = str(kw.pop('end', '\n'))
    if kw:
        raise TypeError("'%s' is an invalid keyword argument for this function" % kw.keys()[0])
    return sep.join(str(a) for a in args) + end