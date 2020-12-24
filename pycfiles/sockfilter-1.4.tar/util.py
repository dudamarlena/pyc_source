# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/sockfilter/sockfilter/util.py
# Compiled at: 2014-07-07 21:25:08


def apply_attr_and_dict(target, key, value):
    if target is None:
        return
    else:
        setattr(target, key, value)
        target.__dict__[key] = value
        return