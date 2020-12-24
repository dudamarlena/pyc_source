# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/collective/ui/ie6nomore/setuphandlers.py
# Compiled at: 2009-08-04 23:53:08


def setupVarious(context):
    if context.readDataFile('collective.ie6nomore_various.txt') is None:
        return
    return