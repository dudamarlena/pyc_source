# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plonetheme/p2/setuphandlers.py
# Compiled at: 2009-05-16 12:06:57


def setupVarious(context):
    if context.readDataFile('plonetheme.p2_various.txt') is None:
        return
    return