# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/issue.py
# Compiled at: 2009-09-03 11:41:06
"""XPointMemo records issue for a XPoint Project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from iscorpio.plonepm.content.xpointdoc import XPointDocument
from iscorpio.plonepm.config import PROJECTNAME
XPointIssueSchema = XPointDocument.schema.copy()
XPointIssueSchema['description'].widget.visible = False
XPointIssueSchema['xpproject_document_status'].required = True
XPointIssueSchema['xpproject_document_status'].widget.visible = True
XPointIssueSchema['xpproject_document_status'].widget.label = 'Issue Status'
XPointIssueSchema['xpproject_document_status'].widget.description = 'Status for this issue.'

class XPointIssue(XPointDocument):
    """ XPointIssue records a issue for a XPoint Project.
    """
    __module__ = __name__
    schema = XPointIssueSchema
    meta_type = 'XPointIssue'
    portal_type = 'XPointIssue'
    archetype_name = 'XP Issue'
    _at_rename_after_creation = True
    security = ClassSecurityInfo()

    def vocabulary_documentStatus(self):
        """ return a list of tuple (status, status desc) for the
        document status select.
        """
        return DisplayList([('open', 'Open'), ('pending', 'Pending'), ('close', 'Close')])


registerType(XPointIssue, PROJECTNAME)