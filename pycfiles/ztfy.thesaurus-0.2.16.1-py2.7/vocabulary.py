# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/vocabulary.py
# Compiled at: 2013-01-30 12:47:15
from zope.schema.interfaces import IVocabularyFactory
from ztfy.thesaurus.interfaces.extension import IThesaurusTermExtension
from ztfy.thesaurus.interfaces.thesaurus import IThesaurus, IThesaurusExtracts
from zope.i18n import translate
from zope.interface import classProvides
from zope.component import getUtilitiesFor
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.traversing.api import getName
from ztfy.utils.request import queryRequest
from ztfy.utils.traversing import getParent
from zope.component.interfaces import ComponentLookupError

class ThesaurusVocabulary(UtilityVocabulary):
    """Thesaurus utilities vocabulary"""
    classProvides(IVocabularyFactory)
    interface = IThesaurus
    nameOnly = False


class ThesaurusNamesVocabulary(UtilityVocabulary):
    """Thesaurus names utilities vocabulary"""
    classProvides(IVocabularyFactory)
    interface = IThesaurus
    nameOnly = True


class ThesaurusExtractsVocabulary(SimpleVocabulary):
    """Thesaurus extracts vocabulary"""
    classProvides(IVocabularyFactory)

    def __init__(self, context=None):
        terms = []
        if context is not None:
            thesaurus = getParent(context, IThesaurus)
            if thesaurus is not None:
                extracts = IThesaurusExtracts(thesaurus)
                terms = [ SimpleTerm(getName(extract), title=extract.name) for extract in extracts.values() ]
                terms.sort(key=lambda x: x.title)
        super(ThesaurusExtractsVocabulary, self).__init__(terms)
        return


class ThesaurusTermExtensionsVocabulary(SimpleVocabulary):
    """Thesaurus term extensions vocabulary"""
    classProvides(IVocabularyFactory)
    interface = IThesaurusTermExtension
    nameOnly = False

    def __init__(self, context, **kw):
        request = queryRequest()
        try:
            utils = getUtilitiesFor(self.interface, context)
            terms = [ SimpleTerm(name, title=translate(util.label, context=request)) for name, util in utils
                    ]
        except ComponentLookupError:
            terms = []

        super(ThesaurusTermExtensionsVocabulary, self).__init__(terms)