# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/collective/indexing/subscribers.py
# Compiled at: 2016-02-28 07:58:27
from zerodb.collective.indexing.queue import getQueue
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import subscribers
from zerodb.models import Model

def zerodb_autoreindex_dispatcher(event):
    if isinstance(event, ObjectModifiedEvent) and isinstance(event.object, Model):
        objectAutoReindex(event)


def objectAutoReindex(ev):
    indexer = getQueue()
    indexer.reindex(ev.object, ev.descriptions)


def init():
    if zerodb_autoreindex_dispatcher not in subscribers:
        subscribers.append(zerodb_autoreindex_dispatcher)