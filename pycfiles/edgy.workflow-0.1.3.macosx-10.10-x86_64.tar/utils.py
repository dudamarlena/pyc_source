# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rd/Work/Edgy/workflow/.virtualenv-python/lib/python2.7/site-packages/edgy/workflow/utils.py
# Compiled at: 2016-02-21 07:40:25
from __future__ import absolute_import, print_function, unicode_literals

def issequence(x):
    return isinstance(x, (tuple, list))