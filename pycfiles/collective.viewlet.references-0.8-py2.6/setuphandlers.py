# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/viewlet/references/setuphandlers.py
# Compiled at: 2010-12-08 06:40:07


def setupVarious(context):
    if context.readDataFile('references_various.txt') is None:
        return
    else:
        return