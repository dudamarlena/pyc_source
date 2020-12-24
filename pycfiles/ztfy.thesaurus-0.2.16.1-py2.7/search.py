# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/browser/json/search.py
# Compiled at: 2013-11-28 04:52:24
from ztfy.thesaurus.interfaces.term import STATUS_ARCHIVED
from ztfy.thesaurus.interfaces.thesaurus import IThesaurus
from z3c.jsonrpc.publisher import MethodPublisher
from zope.component import queryUtility
from ztfy.utils.list import unique

class ThesaurusTermsSearchView(MethodPublisher):
    """Thesaurus terms search view"""

    def findTerms(self, query, thesaurus_name='', extract_name='', autoexpand='on_miss', glob='end', limit=50):
        allow_archives = True
        if IThesaurus.providedBy(self.context):
            thesaurus = self.context
        else:
            thesaurus = queryUtility(IThesaurus, thesaurus_name)
            if thesaurus is None:
                return []
            allow_archives = False
        return [ {'value': term.caption, 'caption': term.caption} for term in unique(thesaurus.findTerms(query, extract_name, autoexpand, glob, limit, exact=True, stemmed=True), idfun=lambda x: x.caption) if allow_archives or term.status != STATUS_ARCHIVED
               ]

    def findTermsWithLabel(self, query, thesaurus_name='', extract_name='', autoexpand='on_miss', glob='end', limit=50):
        allow_archives = True
        if IThesaurus.providedBy(self.context):
            thesaurus = self.context
        else:
            thesaurus = queryUtility(IThesaurus, thesaurus_name)
            if thesaurus is None:
                return []
            allow_archives = False
        return [ {'value': term.label, 'caption': term.label} for term in unique(thesaurus.findTerms(query, extract_name, autoexpand, glob, limit, exact=True, stemmed=True), idfun=lambda x: x.label) if allow_archives or term.status != STATUS_ARCHIVED
               ]