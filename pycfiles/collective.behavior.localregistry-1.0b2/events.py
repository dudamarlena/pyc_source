# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/plone-py2.6/collective/behavior.localregistry/src/collective/behavior/localregistry/events.py
# Compiled at: 2013-04-14 13:39:27
from collective.behavior.localregistry.interfaces import ILocalRegistryCreatedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements

class LocalRegistryCreatedEvent(ObjectEvent):
    implements(ILocalRegistryCreatedEvent)