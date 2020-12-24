# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/theme/setuphandlers.py
# Compiled at: 2009-07-01 06:07:00


def setupVarious(context):
    if context.readDataFile('wwp.theme_various.txt') is None:
        return
    return