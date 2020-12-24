# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/components/cardinality.py
# Compiled at: 2008-09-11 19:48:09
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *
from Products.Archetypes.exceptions import ReferenceException
from Products.Relations import exception, interfaces, ruleset
from Products.Relations.config import *
from Products.Relations.schema import BaseSchemaWithInvisibleId

class CardinalityConstraint(BaseContent, ruleset.RuleBase):
    """An IValidator and IReferenceLayerProvider that enforces cardinality."""
    __module__ = __name__
    __implements__ = BaseContent.__implements__ + (interfaces.IValidator, interfaces.IReferenceLayerProvider)
    content_icon = 'cardinalityconstraint_icon.gif'

    def validateConnected(self, reference, chain):
        self._validate(reference, chain)

    def validateDisconnected(self, reference, chain):
        self._validate(reference, chain)

    def _validate(self, reference, chain):
        rc = getToolByName(self, REFERENCE_CATALOG)
        search_sources = rc(targetUID=reference.targetUID, relationship=reference.relationship)
        search_targets = rc(sourceUID=reference.sourceUID, relationship=reference.relationship)
        sources = len(search_sources)
        targets = len(search_targets)
        self.doValidate(sources, targets, reference, chain)

    def doValidate(self, sources, targets, reference, chain=None):
        rs = self.getRuleset()
        minsc = self.getMinSourceCardinality()
        maxsc = self.getMaxSourceCardinality()
        mintc = self.getMinTargetCardinality()
        maxtc = self.getMaxTargetCardinality()
        if minsc:
            if sources < minsc:
                raise exception.ValidationException("Too few sources (%s) for '%s'." % (sources, rs.Title()), reference, chain)
        if maxsc:
            if sources > maxsc:
                raise exception.ValidationException("Too many sources (%s) for '%s'." % (sources, rs.Title()), reference, chain)
        if mintc:
            if targets < mintc:
                raise exception.ValidationException("Too few targets (%s) for '%s'." % (targets, rs.Title()), reference, chain)
        if maxtc:
            if targets > maxtc:
                raise exception.ValidationException("Too many targets (%s) for '%s'." % (targets, rs.Title()), reference, chain)

    def provideReferenceLayer(self, reference):
        return CardinalityReferenceLayer(self.getRuleset(), self)

    schema = BaseSchemaWithInvisibleId + Schema((IntegerField('minSourceCardinality'), IntegerField('maxSourceCardinality'), IntegerField('minTargetCardinality'), IntegerField('maxTargetCardinality')))
    portal_type = 'Cardinality Constraint'


registerType(CardinalityConstraint)

class CardinalityReferenceLayer:
    __module__ = __name__
    __implements__ = (interfaces.IReferenceLayerProvider,)

    def __init__(self, ruleset, cc):
        self.ruleset = ruleset
        self.component = cc

    def beforeSourceDeleteInformTarget(self, reference):
        rc = getToolByName(self.ruleset, REFERENCE_CATALOG)
        search_sources = rc(targetUID=reference.targetUID, relationship=self.ruleset.getId())
        search_targets = rc(sourceUID=reference.sourceUID, relationship=self.ruleset.getId())
        sources = len(search_sources) - 1
        targets = len(search_targets)
        try:
            self.component.doValidate(sources, targets, reference)
        except exception.ValidationException, e:
            raise ReferenceException, e

    def beforeTargetDeleteInformSource(self, reference):
        rc = getToolByName(self.ruleset, REFERENCE_CATALOG)
        search_sources = rc(targetUID=reference.targetUID, relationship=self.ruleset.getId())
        search_targets = rc(sourceUID=reference.sourceUID, relationship=self.ruleset.getId())
        sources = len(search_sources)
        targets = len(search_targets) - 1
        try:
            self.component.doValidate(sources, targets, reference)
        except exception.ValidationException, e:
            raise ReferenceException, e