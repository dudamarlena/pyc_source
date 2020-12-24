# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alterootheme/lazydays/setuphandlers.py
# Compiled at: 2008-03-31 08:01:01


def setupVarious(context):
    if context.readDataFile('alterootheme.lazydays_various.txt') is None:
        return
    return