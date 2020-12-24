# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/search/content/container.py
# Compiled at: 2008-09-04 04:30:33
from zope.interface import implements
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import registerType
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IFormatable
from easyshop.core.interfaces import ISearchResultContainer

class SearchResultContainer(ATFolder):
    """
    """
    __module__ = __name__
    implements(ISearchResultContainer, IFormatable)


registerType(SearchResultContainer, PROJECTNAME)