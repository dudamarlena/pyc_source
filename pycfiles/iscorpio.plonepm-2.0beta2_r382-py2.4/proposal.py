# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/proposal.py
# Compiled at: 2009-09-03 11:41:06
"""XPointMemo records proposal for a XPoint Project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from iscorpio.plonepm.content.xpointdoc import XPointDocument
from iscorpio.plonepm.config import PROJECTNAME
XPointProposalSchema = XPointDocument.schema.copy()
XPointProposalSchema['description'].widget.visible = False
XPointProposalSchema['xpproject_document_status'].required = True
XPointProposalSchema['xpproject_document_status'].widget.visible = True
XPointProposalSchema['xpproject_document_status'].widget.label = 'Proposal Status'
XPointProposalSchema['xpproject_document_status'].widget.description = 'Status for this proposal.'

class XPointProposal(XPointDocument):
    """ XPointProposal records a proposal for a XPoint Project.
    """
    __module__ = __name__
    schema = XPointProposalSchema
    meta_type = 'XPointProposal'
    portal_type = 'XPointProposal'
    archetype_name = 'XP Proposal'
    _at_rename_after_creation = True
    security = ClassSecurityInfo()

    def vocabulary_documentStatus(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('draft', 'Draft'), ('pending', 'Pending'), ('accepted', 'Accepted')])


registerType(XPointProposal, PROJECTNAME)