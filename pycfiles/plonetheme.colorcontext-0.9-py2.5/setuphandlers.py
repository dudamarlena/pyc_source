# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/colorcontext/setuphandlers.py
# Compiled at: 2010-09-15 08:23:40


def setupVarious(context):
    if context.readDataFile('plonetheme.colorcontext_various.txt') is None:
        return
    return