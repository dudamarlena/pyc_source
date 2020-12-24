# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/workingcopyflag/subscriber.py
# Compiled at: 2012-11-19 05:25:18
from Products.CMFCore.utils import getToolByName
from plone.app.iterate.relation import WorkingCopyRelation
from plone.app.iterate.interfaces import IBaseline

def setFlag(obj, event):
    """Sets workingcopyflag to true, when the item has been checked-in.
    """
    flag = obj.getField('workingcopyflag')
    flag.set(obj, True)
    obj.reindexObject()


def removeFlag(obj, event):
    """Sets workingcopyflag to false, when the item has been checked-out.
    """
    flag = obj.getField('workingcopyflag')
    flag.set(obj, False)
    obj.reindexObject()


def removeFlagOnCancel(obj, event):
    """ Sets workingcopyflag to false on original item, when cancelling.
    """
    relations = obj.getRefs(WorkingCopyRelation.relationship)
    for relation in relations:
        if IBaseline.providedBy(relation):
            flag = relation.getField('workingcopyflag')
            flag.set(relation, False)
            relation.reindexObject()