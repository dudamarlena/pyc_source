# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/adapter.py
# Compiled at: 2013-10-15 10:29:21
from plone.multilingual import interfaces
from plone.uuid.interfaces import IUUIDGenerator
from zope.component import queryUtility
from zope import interface
from zope import component

@interface.implementer(interfaces.ITG)
@component.adapter(interfaces.ITranslatable)
def attributeTG(context):
    return getattr(context, interfaces.ATTRIBUTE_NAME, None)


class MutableAttributeTG(object):
    interface.implements(interfaces.IMutableTG)
    component.adapts(interfaces.ITranslatable)

    def __init__(self, context):
        self.context = context

    def get(self):
        return getattr(self.context, interfaces.ATTRIBUTE_NAME, None)

    def set(self, tg):
        if tg == interfaces.NOTG:
            generator = queryUtility(IUUIDGenerator)
            tg = generator()
        tg = str(tg)
        setattr(self.context, interfaces.ATTRIBUTE_NAME, tg)