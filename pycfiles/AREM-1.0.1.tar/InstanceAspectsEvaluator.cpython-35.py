# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/InstanceAspectsEvaluator.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 1917 bytes
__doc__ = '\nCreated on May 12, 2011\n\n@author: Mark V Systems Limited\n(c) Copyright 2011 Mark V Systems Limited, All rights reserved.\n'
from collections import defaultdict
import os, datetime
from arelle import ModelObject

def setup(view):
    relsSet = view.modelXbrl.relationshipSet(view.arcrole, view.linkrole, view.linkqname, view.arcqname)
    view.concepts = set(fact.concept for fact in view.modelXbrl.facts)
    view.linkroles = set(rel.linkrole for c in view.concepts for rels in (
     relsSet.fromModelObject(c), relsSet.toModelObject(c)))


def setupLinkrole(view, linkrole):
    view.linkrole = linkrole
    relsSet = view.modelXbrl.relationshipSet(view.arcrole, view.linkrole, view.linkqname, view.arcqname)
    concepts = set(c for c in view.concepts if relsSet.fromModelObject(c) or relsSet.toModelObject(c))
    facts = set(f for f in view.modelXbrl.facts if f.concept in concepts)
    contexts = set(f.context for f in facts)
    view.periodContexts = defaultdict(set)
    contextStartDatetimes = {}
    view.dimensionMembers = defaultdict(set)
    view.entityIdentifiers = set()
    for context in contexts:
        if context.isForeverPeriod:
            contextkey = datetime.datetime(datetime.MINYEAR, 1, 1)
        else:
            contextkey = context.endDatetime
        objectId = context.objectId()
        view.periodContexts[contextkey].add(objectId)
        if context.isStartEndPeriod:
            contextStartDatetimes[objectId] = context.startDatetime
        view.entityIdentifiers.add(context.entityIdentifier[1])
        for modelDimension in context.qnameDims.values():
            if modelDimension.isExplicit:
                view.dimensionMembers[modelDimension.dimension] = modelDimension.member

    view.periodKeys = list(view.periodContexts.keys())
    view.periodKeys.sort()