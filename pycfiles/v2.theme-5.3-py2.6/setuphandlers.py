# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/v2/theme/setuphandlers.py
# Compiled at: 2010-11-24 05:03:52


def setupVarious(context):
    if context.readDataFile('v2.theme_various.txt') is None:
        return
    else:
        return