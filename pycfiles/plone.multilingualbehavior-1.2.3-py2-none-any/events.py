# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/events.py
# Compiled at: 2013-10-15 10:29:21
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'
from zope.interface import implements
from zope.interface import Attribute
from zope.component.interfaces import IObjectEvent

class IObjectWillBeTranslatedEvent(IObjectEvent):
    """Sent before an object is translated."""
    object = Attribute('The object to be translated.')
    language = Attribute('Target language.')


class IObjectTranslatedEvent(IObjectEvent):
    """Sent after an object was translated."""
    object = Attribute('The object to be translated.')
    target = Attribute('The translation target object.')
    language = Attribute('Target language.')


class ObjectWillBeTranslatedEvent(object):
    """Sent before an object is translated."""
    implements(IObjectWillBeTranslatedEvent)

    def __init__(self, context, language):
        self.object = context
        self.language = language


class ObjectTranslatedEvent(object):
    """Sent after an object was translated."""
    implements(IObjectTranslatedEvent)

    def __init__(self, context, target, language):
        self.object = context
        self.target = target
        self.language = language