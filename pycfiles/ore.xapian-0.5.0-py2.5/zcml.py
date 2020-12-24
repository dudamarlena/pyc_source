# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/zcml.py
# Compiled at: 2008-09-22 22:53:39
from zope.interface import Interface
from zope.configuration.fields import GlobalObject
from ore.xapian import MessageFactory as _
from ore.xapian import queue
import interfaces

class IQueueDirective(Interface):
    indexer = GlobalObject(title=_('Xapian indexer'), required=True)


def queueDirective(_context, indexer):
    if interfaces.DEBUG_SYNC:
        return
    queue.QueueProcessor.start(indexer, silent=True)