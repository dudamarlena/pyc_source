# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/release.py
# Compiled at: 2009-09-03 11:41:06
"""XPointRelease defines the release note for a XPoint Project."""
__author__ = 'iScorpio <iscorpio@users.sourceforge.net>'
__docformat__ = 'plaintext'
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import registerType
from iscorpio.plonepm.content.xpointdoc import XPointDocument
from iscorpio.plonepm.config import PROJECTNAME
XPointReleaseSchema = XPointDocument.schema.copy()

class XPointRelease(XPointDocument):
    """ XPointRelease will hold a release note for a XPoint Project.
    """
    __module__ = __name__
    schema = XPointReleaseSchema
    meta_type = 'XPointRelease'
    portal_type = 'XPointRelease'
    archetype_name = 'XP Release'
    _at_rename_after_creation = True
    security = ClassSecurityInfo()


registerType(XPointRelease, PROJECTNAME)