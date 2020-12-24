# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/workingcopyflag/interfaces.py
# Compiled at: 2012-11-19 05:25:18
from zope.interface import Interface

class IWorkingcopyFlaggableObject(Interface):
    """Marker interface for marking an object with a workingcopy as flagged"""
    pass