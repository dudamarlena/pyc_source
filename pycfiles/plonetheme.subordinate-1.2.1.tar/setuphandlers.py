# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/stylized/setuphandlers.py
# Compiled at: 2008-10-23 16:07:07


def setupVarious(context):
    if context.readDataFile('plonetheme.stylized_various.txt') is None:
        return
    return