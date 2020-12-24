# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMIteration.py
# Compiled at: 2009-09-24 04:22:00
"""
An iteration for a project could be a phase or a release.  Basically, we want
the period of an iteration as small as possible.
"""
import logging
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.content.base import XPPMBase
from iscorpio.plonepm.interfaces import IPPMIteration
__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'
PPMIterationSchema = ATCTContent.schema.copy() + Schema((TextField('xppm_text', searchable=True, required=True, default_output_type='text/x-html-safe', widget=RichWidget(label='Iteration Plan', description='The details plan about this iteration.', rows=25)), DateTimeField('xppm_completion_date', searchable=False, required=True, widget=CalendarWidget(label='Target Completion Date', description='Specify the date when this iteration should be completed', show_hm=False))))
finalizeATCTSchema(PPMIterationSchema)
PPMIterationSchema['description'].widget.visible = False

class PPMIteration(XPPMBase, ATCTContent, HistoryAwareMixin):
    """
    defines a iteration for ppm project.
    """
    __module__ = __name__
    schema = PPMIterationSchema
    meta_type = 'PPMIteration'
    portal_type = 'PPMIteration'
    archetypes_type = 'PPMIteration'
    __implements__ = (
     ATCTContent.__implements__, HistoryAwareMixin.__implements__)
    implements(IPPMIteration)
    xppm_id_prefix = 'xpi'
    log = logging.getLogger('PlonePM PPMIteration')
    security = ClassSecurityInfo()
    security.declarePublic('getIterationStories')

    def getIterationStories(self):
        """
        returns all stories for this iteration.
        """
        return self.getAllStories(iteration=self.id)


registerType(PPMIteration, PROJECTNAME)