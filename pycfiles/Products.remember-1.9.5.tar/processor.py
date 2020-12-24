# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/processor.py
# Compiled at: 2008-09-11 19:48:09
import transaction
from AccessControl import ModuleSecurityInfo
from Products.CMFCore.utils import getToolByName
from config import *
import brain, interfaces
from events import RelationConnectedEvent
from events import RelationDisconnectedEvent
from zope.event import notify
modulesec = ModuleSecurityInfo('Products.Relations.processor')

class Chain(dict):
    __module__ = __name__
    __implements__ = (interfaces.IChain,)

    def __init__(self):
        self.added = []
        self.deleted = []

    def __getitem__(self, key):
        if key not in self.keys():
            self[key] = {}
        return dict.__getitem__(self, key)


__implements__ = (
 interfaces.IReferenceConnectionProcessor,)
modulesec.declarePublic('process')

def process(context, connect=(), disconnect=()):
    sp = transaction.savepoint()
    try:
        return _process(context, connect, disconnect)
    except:
        sp.rollback()
        raise


def _process(context, connect, disconnect):
    library = getToolByName(context, RELATIONS_LIBRARY)
    ref_ctl = getToolByName(context, REFERENCE_CATALOG)
    chain = Chain()
    seen_rulesets = {}
    connectEvents = list()
    disconnectEvents = list()
    for (sUID, tUID, relationship) in connect:
        chainstart = len(chain.added)
        ruleset = _lookup(relationship, library, seen_rulesets)
        sbrain = brain.makeBrainAggregate(context, sUID)
        tbrain = brain.makeBrainAggregate(context, tUID)
        ruleset.implyOnConnect(sbrain, tbrain, chain)
        connected = chain.added[chainstart:]
        if connected != []:
            connectEvents.append(RelationConnectedEvent(context, connected))

    for item in disconnect:
        chainstart = len(chain.deleted)
        if not isinstance(item, str):
            (sUID, tUID, relationship) = item
            ruleset = _lookup(relationship, library, seen_rulesets)
            refs = ref_ctl(sourceUID=sUID, targetUID=tUID, relationship=relationship)
            if refs:
                ruleset.implyOnDisconnect(refs[0].getObject(), chain)
        else:
            rUID = item
            refs = ref_ctl(UID=rUID) or []
            if refs:
                ref = refs[0]
                ruleset = _lookup(ref.relationship, library, seen_rulesets)
                ruleset.implyOnDisconnect(refs[0].getObject(), chain)
        disconnected = chain.deleted[chainstart:]
        if disconnected != []:
            disconnectEvents.append(RelationDisconnectedEvent(context, disconnected))

    _validate(context, chain, seen_rulesets)
    sp = transaction.savepoint()
    for event in disconnectEvents:
        notify(event)

    _finalize(context, chain, seen_rulesets)
    sp = transaction.savepoint()
    for event in connectEvents:
        notify(event)

    return chain


def _validate(context, chain, seen_rulesets):
    library = getToolByName(context, RELATIONS_LIBRARY)
    for reference in chain.added:
        ruleset = _lookup(reference.relationship, library, seen_rulesets)
        ruleset.validateConnected(reference, chain)

    for reference in chain.deleted:
        ruleset = _lookup(reference.relationship, library, seen_rulesets)
        ruleset.validateDisconnected(reference, chain)


def _finalize(context, chain, seen_rulesets):
    library = getToolByName(context, RELATIONS_LIBRARY)
    for reference in chain.added:
        ruleset = _lookup(reference.relationship, library, seen_rulesets)
        ruleset.finalizeOnConnect(reference, chain)

    for reference in chain.deleted:
        ruleset = _lookup(reference.relationship, library, seen_rulesets)
        ruleset.finalizeOnDisconnect(reference, chain)


def _lookup(relationship, library, seen_rulesets):
    if not seen_rulesets.has_key(relationship):
        seen_rulesets[relationship] = library.getRuleset(relationship)
    return seen_rulesets[relationship]