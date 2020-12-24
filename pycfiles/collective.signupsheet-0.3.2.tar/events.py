# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/signableevent/events.py
# Compiled at: 2011-07-29 07:55:08
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from collective.signableevent.interfaces import ISignupAddedEvent

class SignupAddedEvent(ObjectModifiedEvent):
    """ """
    implements(ISignupAddedEvent)