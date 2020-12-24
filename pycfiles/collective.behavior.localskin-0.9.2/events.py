# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/plone-py2.6/collective/behavior.localregistry/src/collective/behavior/localregistry/events.py
# Compiled at: 2013-04-14 13:39:27
from collective.behavior.localregistry.interfaces import ILocalRegistryCreatedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements

class LocalRegistryCreatedEvent(ObjectEvent):
    implements(ILocalRegistryCreatedEvent)