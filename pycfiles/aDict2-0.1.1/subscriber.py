# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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