# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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