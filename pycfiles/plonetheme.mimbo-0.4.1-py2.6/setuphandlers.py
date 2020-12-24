# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/mimbo/setuphandlers.py
# Compiled at: 2009-12-03 13:27:27


def setupVarious(context):
    if context.readDataFile('plonetheme.mimbo_various.txt') is None:
        return
    else:
        return