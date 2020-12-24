# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/ely/advancedquery/interfaces.py
# Compiled at: 2008-06-10 17:05:54
from zope.interface import Interface

class IAdvancedCatalogQuery(Interface):
    """
    A utility to use the Advanced Query extension to Zope's Zcatalog
    in a plone site.
    """
    __module__ = __name__

    def __call__(query):
        """
        execute the query on the portal catalog
        """
        pass