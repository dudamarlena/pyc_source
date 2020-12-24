# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/signableevent/events.py
# Compiled at: 2011-07-29 07:55:08
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from collective.signableevent.interfaces import ISignupAddedEvent

class SignupAddedEvent(ObjectModifiedEvent):
    """ """
    implements(ISignupAddedEvent)