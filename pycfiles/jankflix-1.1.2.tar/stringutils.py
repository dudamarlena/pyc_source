# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/workspace_py/jankflix-python/jankflixmodules/utils/stringutils.py
# Compiled at: 2013-01-14 12:24:22


def get_after(string, after_this):
    return string[string.index(after_this) + len(after_this):]


def get_before(string, before_this):
    return string[:string.index(before_this)]