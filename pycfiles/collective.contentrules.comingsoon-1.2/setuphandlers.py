# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentmigrationui/setuphandlers.py
# Compiled at: 2010-08-19 03:33:06


def setupVarious(context):
    if context.readDataFile('collective.contentmigrationui_various.txt') is None:
        return
    return