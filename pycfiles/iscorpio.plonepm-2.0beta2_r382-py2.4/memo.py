# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/memo.py
# Compiled at: 2009-09-03 11:41:06
"""XPointMemo defines the memo for a XPoint Project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import registerType
from iscorpio.plonepm.content.xpointdoc import XPointDocument
from iscorpio.plonepm.config import PROJECTNAME
XPointMemoSchema = XPointDocument.schema.copy()
XPointMemoSchema['description'].widget.visible = False

class XPointMemo(XPointDocument):
    """ XPointMemo defines the note for a XPoint Project.
    """
    __module__ = __name__
    schema = XPointMemoSchema
    meta_type = 'XPointMemo'
    portal_type = 'XPointMemo'
    archetype_name = 'XP Memo'
    _at_rename_after_creation = True
    security = ClassSecurityInfo()


def modify_fti(fti):
    for a in fti['actions']:
        if a['id'] in ['metadata']:
            a['visible'] = 0

    return fti


registerType(XPointMemo, PROJECTNAME)