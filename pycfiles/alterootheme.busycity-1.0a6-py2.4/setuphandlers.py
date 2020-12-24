# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alterootheme/busycity/setuphandlers.py
# Compiled at: 2008-03-21 08:10:00


def setupVarious(context):
    if context.readDataFile('alterootheme.busycity_various.txt') is None:
        return
    return