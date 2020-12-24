# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/preferences.py
# Compiled at: 2008-10-06 10:31:12
from zope.interface import implements
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
import interfaces

class icSemanticManagementAdvancedSearchOptions(SimpleItem):
    __module__ = __name__
    implements(interfaces.IicSemanticManagementAdvancedSearchOptions)
    include_ontocatalog_criteria = FieldProperty(interfaces.IicSemanticManagementAdvancedSearchOptions['include_ontocatalog_criteria'])

    def __call__(self):
        pass


def advanced_search_form_adapter(context):
    return getUtility(interfaces.IicSemanticManagementAdvancedSearchOptions, name='icsemantic.advancedsearch', context=context)