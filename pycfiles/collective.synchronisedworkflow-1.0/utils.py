# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/utils.py
# Compiled at: 2008-12-16 18:21:21
from zope.interface import implements
from events import SynchroModifiedEvent
from events import SynchroDeletedEvent
from zope.event import notify

def notify_modified(context):
    notify(SynchroModifiedEvent(context))


def notify_deleted(context):
    notify(SynchroDeletedEvent(context))