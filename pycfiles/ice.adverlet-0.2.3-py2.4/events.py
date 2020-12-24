# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/events.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope import event
from zope.interface import implements
from interfaces import ISourceModifiedEvent

class SourceModifiedEvent:
    __module__ = __name__
    implements(ISourceModifiedEvent)

    def __init__(self, name):
        self.name = name