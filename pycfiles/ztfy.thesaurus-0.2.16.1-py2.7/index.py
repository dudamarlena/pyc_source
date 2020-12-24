# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/interfaces/index.py
# Compiled at: 2013-12-17 10:06:45
from zope.interface import Interface
from zope.schema import TextLine, Bool
from ztfy.thesaurus import _

class IThesaurusTermFieldIndex(Interface):
    """Thesaurus term field index interface"""
    include_parents = Bool(title=_('Include term parents into index values'), default=False, required=False)
    include_synonyms = Bool(title=_('Include term synonyms into index values'), default=False, required=False)


class IThesaurusTermsListFieldIndex(Interface):
    """Thesaurus terms list field index interface"""
    include_parents = Bool(title=_('Include term parents into index values'), default=False, required=False)
    include_synonyms = Bool(title=_('Include term synonyms into index values'), default=False, required=False)