# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/components/types.py
# Compiled at: 2008-09-11 19:48:09
__doc__ = 'Components that validate against types and interfaces.'
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *
from Products.Relations import brain, exception, ruleset, interfaces, utils
from Products.Relations.config import *
from Products.Relations.schema import BaseSchemaWithInvisibleId

class PortalTypeConstraint(BaseContent, ruleset.RuleBase):
    """A validator and vocabulary provider, restricting sources and targets
    by portal type."""
    __module__ = __name__
    __implements__ = (
     interfaces.IVocabularyProvider, interfaces.IValidator) + BaseContent.__implements__
    content_icon = 'portaltypeconstraint_icon.gif'

    def makeVocabulary(self, source, targets=None):
        ast = self.getAllowedSourceTypes()
        att = self.getAllowedTargetTypes()
        if ast and source.portal_type not in ast:
            return []
        if targets is not None:
            return [ t for t in targets if not att or t.portal_type in att ]
        else:
            uc = getToolByName(self, UID_CATALOG)
            objs = uc(**self.getSearchTerms())
            return [ brain.makeBrainAggregate(self, o) for o in objs ]
        return

    def getSearchTerms(self):
        d = {}
        att = self.getAllowedTargetTypes()
        if att:
            d['portal_type'] = att
        return d

    def validateConnected(self, reference, chain):
        ast = self.getAllowedSourceTypes()
        att = self.getAllowedTargetTypes()
        st = reference.getSourceBrain().portal_type
        tt = reference.getTargetBrain().portal_type
        if ast:
            if st not in ast:
                raise exception.ValidationException("Source type %s not allowed for '%s'." % (st, self.getRuleset().Title()), reference, chain)
        if att:
            if tt not in att:
                raise exception.ValidationException("Target type %s not allowed for '%s'." % (tt, self.getRuleset().Title()), reference, chain)

    def validateDisconnected(self, reference, chain):
        """Don't care."""
        pass

    schema = BaseSchemaWithInvisibleId + Schema((LinesField('allowedSourceTypes', vocabulary='_allowedTypesVocabulary', enforceVocabulary=True, widget=MultiSelectionWidget), LinesField('allowedTargetTypes', vocabulary='_allowedTypesVocabulary', enforceVocabulary=True, widget=MultiSelectionWidget)))
    portal_type = 'Type Constraint'

    def _allowedTypesVocabulary(self):
        return DisplayList([ (pt, pt) for pt in utils.getReferenceableTypes(self) ])


registerType(PortalTypeConstraint)

class InterfaceConstraint(PortalTypeConstraint):
    """A validator and vocabulary provider, restricting sources and targets
    by interfaces they implement."""
    __module__ = __name__

    def getAllowedSourceTypes(self):
        asi = self.getAllowedSourceInterfaces()
        if asi:
            return self._getPortalTypesByInterfaces(asi)
        else:
            return []

    def getAllowedTargetTypes(self):
        ati = self.getAllowedTargetInterfaces()
        if ati:
            return self._getPortalTypesByInterfaces(ati)
        else:
            return []

    def _getPortalTypesByInterfaces(self, allowed):
        portal_types = utils.getPortalTypesByInterfaces(self, allowed)
        portal_types.append('spam')
        return portal_types

    schema = BaseSchemaWithInvisibleId + Schema((LinesField('allowedSourceInterfaces'), LinesField('allowedTargetInterfaces')))
    archetype_name = portal_type = 'Interface Constraint'


registerType(InterfaceConstraint)