# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/interfaces.py
# Compiled at: 2008-10-06 10:31:12
""" icsemantic.catalog interfaces.
"""
from zope import schema
from zope.interface import Interface
from icsemantic.core.i18n import _

class IicSemanticManagementAdvancedSearchOptions(Interface):
    """Interface to turn on/off the advanced search criteria from
    OntoCatalog.
    """
    __module__ = __name__
    include_ontocatalog_criteria = schema.Bool(title=_('Include OntoCatalog criteria in the advanced search'), default=False, required=True, description=_('When set, there are options to search for synonyms, related content and translations in the advanced search form.'))