# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/weight.py
# Compiled at: 2008-09-03 11:14:39
from zope.interface import implements
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IWeightCriteria
schema = Schema((FloatField(name='weight', default=0.0, widget=DecimalWidget(label='Weight', label_msgid='schema_weight_label', description='The weight of the cart', description_msgid='schema_weight_description', i18n_domain='EasyShop')),))

class WeightCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(IWeightCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return 'Weight'

    def getValue(self):
        """
        """
        return self.getWeight()


registerType(WeightCriteria, PROJECTNAME)