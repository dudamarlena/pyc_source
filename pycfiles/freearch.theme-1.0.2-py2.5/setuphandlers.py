# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freearch/theme/setuphandlers.py
# Compiled at: 2008-06-18 04:52:12


def setupVarious(context):
    if context.readDataFile('freearch.theme_various.txt') is None:
        return
    return