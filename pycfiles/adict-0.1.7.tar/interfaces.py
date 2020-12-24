# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/workingcopyflag/interfaces.py
# Compiled at: 2012-11-19 05:25:18
from zope.interface import Interface

class IWorkingcopyFlaggableObject(Interface):
    """Marker interface for marking an object with a workingcopy as flagged"""