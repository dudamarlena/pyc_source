# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/kupuemoticons/setuphandlers.py
# Compiled at: 2008-08-27 06:14:50
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

def setupVarious(context):
    if context.readDataFile('collective.kupuemoticons_various.txt') is None:
        return
    return