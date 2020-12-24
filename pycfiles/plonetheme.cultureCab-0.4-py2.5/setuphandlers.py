# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/cultureCab/setuphandlers.py
# Compiled at: 2010-09-22 06:02:54


def setupVarious(context):
    if context.readDataFile('plonetheme.cultureCab_various.txt') is None:
        return
    return