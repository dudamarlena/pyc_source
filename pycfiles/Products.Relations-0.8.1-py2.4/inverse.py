# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/components/inverse.py
# Compiled at: 2008-09-11 19:48:09
from Acquisition import ImplicitAcquisitionWrapper, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *
from Products.Archetypes.ReferenceEngine import Reference
from Products.Archetypes.utils import make_uuid
from Products.Relations.config import *
from Products.Relations import interfaces, ruleset, utils
from Products.Relations.schema import BaseSchemaWithInvisibleId
_invref_attr = '_relations_invref_uid'
_proc_marker_attr = '_v_relations_process_invref'

class InverseImplicator(BaseContent, ruleset.RuleBase):
    """Implicator that creates a reference from target to source."""
    __module__ = __name__
    __implements__ = (
     interfaces.IImplicator,) + BaseContent.__implements__
    content_icon = 'inverseimplicator_icon.gif'

    def implyOnConnect(self, reference, chain):
        iRuleset = self.getInverseRuleset()
        if iRuleset is not None and not hasattr(reference, _proc_marker_attr):
            added_index = len(chain.added)
            iRuleset.implyOnConnect(reference.getTargetBrain(), reference.getSourceBrain(), chain, metadata={_proc_marker_attr: True})
            invRef = chain.added[added_index]
            setattr(reference, _invref_attr, invRef.UID())
            setattr(invRef, _invref_attr, reference.UID())
        return

    def implyOnDisconnect(self, reference, chain):
        mykey = '%s:disconnected' % self.__class__.__name__
        ref_catalog = getToolByName(self, REFERENCE_CATALOG)
        iRuleset = self.getInverseRuleset()
        if iRuleset is not None and reference.UID() not in chain[mykey]:
            chain[mykey][reference.UID()] = reference
            invRefUID = getattr(reference, _invref_attr)
            brains = ref_catalog(UID=invRefUID)
            if brains:
                invRef = brains[0].getObject()
                iRuleset.implyOnDisconnect(invRef, chain)
        return

    schema = BaseSchemaWithInvisibleId + Schema((ReferenceField('inverseRuleset', relationship='inverseRuleset', allowed_types_method='_allowedTypesRuleset'),))
    portal_type = 'Inverse Implicator'

    def _allowedTypesRuleset(self, instance):
        return utils.getPortalTypesByInterfaces(self, ('IRuleset', ))

    def getInverseRuleset(self):
        inv = self.getRefs('inverseRuleset')
        if inv:
            return inv[0]
        else:
            return
        return


registerType(InverseImplicator)