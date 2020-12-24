# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/utils/password.py
# Compiled at: 2018-11-28 03:20:09
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
from pocsuite.lib.core.common import getFileItems
from pocsuite.lib.core.data import paths

def getWeakPassword():
    return getFileItems(paths.WEAK_PASS)


def getLargeWeakPassword():
    return getFileItems(paths.LARGE_WEAK_PASS)