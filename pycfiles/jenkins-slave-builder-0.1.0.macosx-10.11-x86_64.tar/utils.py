# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nakagawa.masaki/.pyenv/versions/2.7.11/lib/python2.7/site-packages/builder/utils.py
# Compiled at: 2016-05-23 03:45:17
import re

def camelize(thing):
    return re.sub('_(.)', lambda x: x.group(1).upper(), thing)