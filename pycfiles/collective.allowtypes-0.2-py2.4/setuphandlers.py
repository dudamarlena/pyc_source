# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/allowtypes/setuphandlers.py
# Compiled at: 2008-11-10 16:09:04
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

def importVarious(context):
    if context.readDataFile('allowtypes.txt') is None:
        return
    return