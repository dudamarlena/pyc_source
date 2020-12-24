# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/analysis.py
# Compiled at: 2014-12-12 07:13:54
from Products.Archetypes import atapi
from bika.lims.config import PROJECTNAME as BIKALIMS_PROJECTNAME
from bika.lims.content.analysis import Analysis as BaseAnalysis
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.lims.interfaces import IAnalysis
from zope.component import adapts
from zope.interface import implements

class AnalysisSchemaExtender(object):
    adapts(IAnalysis)
    implements(ISchemaExtender)
    fields = []

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class Analysis(BaseAnalysis):
    """ Inherits from bika.lims.content.Analysis
    """
    pass


atapi.registerType(Analysis, BIKALIMS_PROJECTNAME)