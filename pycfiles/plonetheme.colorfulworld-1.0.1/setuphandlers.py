# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/colorcontext/setuphandlers.py
# Compiled at: 2010-09-15 08:23:40


def setupVarious(context):
    if context.readDataFile('plonetheme.colorcontext_various.txt') is None:
        return
    return