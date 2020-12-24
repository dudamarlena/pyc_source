# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/handlers.py
# Compiled at: 2013-10-15 10:29:21
from zope.component import adapter
from zope.component import queryUtility
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectCopiedEvent
from plone.uuid.interfaces import IUUIDGenerator
from plone.multilingual.interfaces import ATTRIBUTE_NAME, ITranslatable
try:
    from Acquisition import aq_base
except ImportError:
    aq_base = lambda v: v

@adapter(ITranslatable, IObjectCreatedEvent)
def addAttributeTG(obj, event):
    if not IObjectCopiedEvent.providedBy(event):
        if getattr(aq_base(obj), ATTRIBUTE_NAME, None):
            return
    generator = queryUtility(IUUIDGenerator)
    if generator is None:
        return
    else:
        tg = generator()
        if not tg:
            return
        setattr(obj, ATTRIBUTE_NAME, tg)
        return