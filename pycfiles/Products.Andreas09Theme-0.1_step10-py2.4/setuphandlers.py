# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/Andreas09Theme/setuphandlers.py
# Compiled at: 2008-09-09 18:26:37


def setupVarious(context):
    if context.readDataFile('Products.Andreas09Theme_various.txt') is None:
        return
    return