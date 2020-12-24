# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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