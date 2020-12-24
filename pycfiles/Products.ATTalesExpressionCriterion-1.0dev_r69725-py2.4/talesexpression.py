# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/ATTalesExpressionCriterion/criteria/talesexpression.py
# Compiled at: 2008-07-28 08:20:38
""" Topic:

"""
__author__ = 'Andreas Gabriel <gabriel@hrz.uni-marburg.de>'
__docformat__ = 'restructuredtext'
from Products.CMFCore.permissions import View
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import Schema, registerType
from Products.TALESField import TALESString
from Products.Archetypes.atapi import StringWidget
from Products.ATContentTypes.criteria import _criterionRegistry, registerCriterion, STRING_INDICES
from Products.ATContentTypes.interfaces import IATTopicSearchCriterion
from Products.ATContentTypes.permission import ChangeTopics
from Products.ATContentTypes.criteria.base import ATBaseCriterion
from Products.ATContentTypes.criteria.schemata import ATBaseCriterionSchema
from Products.ATTalesExpressionCriterion import ATTalesExpressionCriterionMessageFactory as _
from Products.ATTalesExpressionCriterion.config import PROJECTNAME
ATTalesExpressionCriterionSchema = ATBaseCriterionSchema + Schema((TALESString('value', required=1, mode='rw', write_permission=ChangeTopics, accessor='Value', mutator='setValue', widget=StringWidget(label=_('label_tales_criteria_value', default='Value'), description=_('help_tales_criteria_value', default='A tales expression.'))),))

class ATTalesExpressionCriterion(ATBaseCriterion):
    """A tales expression criterion"""
    __module__ = __name__
    __implements__ = ATBaseCriterion.__implements__ + (IATTopicSearchCriterion,)
    security = ClassSecurityInfo()
    schema = ATTalesExpressionCriterionSchema
    meta_type = 'ATTalesExpressionCriterion'
    archetype_name = 'Tales Expression Criterion'
    shortDesc = 'Expression'
    security.declareProtected(View, 'getCriteriaItems')

    def getCriteriaItems(self):
        result = []
        if self.Value() is not '':
            result.append((self.Field(), self.Value()))
        return tuple(result)


registerCriterion(ATTalesExpressionCriterion, STRING_INDICES)