# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/analysis/resultoutofrange.py
# Compiled at: 2014-12-12 07:13:54
from Products.CMFCore.utils import getToolByName
from bika.lims import bikaMessageFactory as _
from bika.lims.interfaces import IAnalysis
from bika.lims.interfaces import IFieldIcons
from bika.lims.permissions import *
from zope.interface import implements
from zope.component import adapts

class ResultOutOfRange(object):
    """An alert provider for Analysis results outside of panic ranges
    """
    implements(IFieldIcons)
    adapts(IAnalysis)

    def __init__(self, context):
        self.context = context

    def __call__(self, result=None, specification=None, **kwargs):
        """ Check if result value is 'in panic'.
        """
        analysis = self.context
        path = '++resource++bika.health.images'
        translate = self.context.translate
        workflow = getToolByName(self.context, 'portal_workflow')
        astate = workflow.getInfoFor(analysis, 'review_state')
        if astate == 'retracted':
            return {}
        else:
            result = result is not None and str(result) or analysis.getResult()
            if result == '':
                return {}
            try:
                result = float(str(result))
            except ValueError:
                return {}

            specs = hasattr(analysis, 'getAnalysisSpecs') and analysis.getAnalysisSpecs(specification) or None
            spec_min = None
            spec_max = None
            if specs is None:
                return {}
            keyword = analysis.getService().getKeyword()
            spec = specs.getResultsRangeDict()
            if keyword in spec:
                try:
                    spec_min = float(spec[keyword]['minpanic'])
                except:
                    spec_min = None

                try:
                    spec_max = float(spec[keyword]['maxpanic'])
                except:
                    spec_max = None

                if not spec_min and not spec_max:
                    outofrange, acceptable, o_spec = False, None, None
                elif spec_min and spec_max and spec_min <= result <= spec_max:
                    outofrange, acceptable, o_spec = False, None, None
                elif spec_min and not spec_max and spec_min <= result:
                    outofrange, acceptable, o_spec = False, None, None
                elif not spec_min and spec_max and spec_max >= result:
                    outofrange, acceptable, o_spec = False, None, None
                else:
                    outofrange, acceptable, o_spec = True, False, spec[keyword]
            else:
                outofrange, acceptable, o_spec = False, None, None
            alerts = {}
            if outofrange:
                range_str = ('{0} {1}, {2} {3}').format(translate(_('minpanic')), str(o_spec['minpanic']), translate(_('maxpanic')), str(o_spec['maxpanic']))
                if acceptable:
                    message = ('{0} ({1})').format(translate(_('Result in shoulder panic range')), range_str)
                else:
                    message = ('{0} ({1})').format(translate(_('Result exceeded panic level')), range_str)
                alerts[analysis.UID()] = [
                 {'msg': message, 
                    'icon': path + '/lifethreat.png', 
                    'field': 'Result'}]
            return alerts