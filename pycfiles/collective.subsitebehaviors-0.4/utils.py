# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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