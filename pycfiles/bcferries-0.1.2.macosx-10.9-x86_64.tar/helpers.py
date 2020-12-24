# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/bcferries/lib/python2.7/site-packages/bcferries/helpers.py
# Compiled at: 2014-12-29 10:34:30


def to_int(s):
    try:
        return max(int(s), 0)
    except:
        return 0