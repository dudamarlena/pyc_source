# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /media/psf/Home/Code/koodaamo/collective.subsitebehaviors/src/collective/subsitebehaviors/utils.py
# Compiled at: 2015-02-08 13:17:58
from itertools import chain
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.schema import getFieldsInOrder
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.interfaces import IDexterityFTI

def all_dexterity_fieldnames(obj):
    """the schema from FTI plus query IBehaviorAssignable"""
    try:
        typename = obj.getPortalTypeName()
        fti = getUtility(IDexterityFTI, name=typename)
    except ComponentLookupError as exc:
        return []

    schema = fti.lookupSchema()
    fields = [getFieldsInOrder(schema)]
    behavior_assignable = IBehaviorAssignable(obj)
    if behavior_assignable:
        behaviors = behavior_assignable.enumerateBehaviors()
        for behavior in behaviors:
            fields.append(getFieldsInOrder(behavior.interface))

    return [ fn for fn, f in chain(*fields) ]