# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/browser/traverser.py
# Compiled at: 2012-04-06 05:41:47
from ztfy.thesaurus.interfaces.thesaurus import IThesaurus, IThesaurusExtracts
from zope.component import getUtility
from zope.traversing.namespace import view

class ThesaurusManagerNamespaceTraverser(view):
    """++thesaurus++ namespace traverser"""

    def traverse(self, name, ignored):
        return getUtility(IThesaurus, name)


class ThesaurusExtractsNamespaceTraverser(view):
    """++extracts++ namespace traverser"""

    def traverse(self, name, ignored):
        return IThesaurusExtracts(IThesaurus(self.context))


class ThesaurusTermsNamespaceTraverser(view):
    """++terms++ namespace traverser"""

    def traverse(self, name, ignored):
        return IThesaurus(self.context).terms


class ThesaurusCatalogNamespaceTraverser(view):
    """++catalog++ namespace traverser"""

    def traverse(self, name, ignored):
        return IThesaurus(self.context).catalog