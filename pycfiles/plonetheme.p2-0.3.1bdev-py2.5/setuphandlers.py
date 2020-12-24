# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plonetheme/p2/setuphandlers.py
# Compiled at: 2009-05-16 12:06:57


def setupVarious(context):
    if context.readDataFile('plonetheme.p2_various.txt') is None:
        return
    return