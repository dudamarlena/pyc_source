# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/setuphandlers.py
# Compiled at: 2017-09-19 09:07:49
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.ATVocabularyManager.utils.vocabs import createHierarchicalVocabs
from land.copernicus.content.content.vocabulary import COUNTRIES_DICTIONARY_ID
from land.copernicus.content.content.vocabulary import getCountriesDictionary
import logging
logger = logging.getLogger('land.copernicus.content: setuphandlers')

def installVocabularies(context):
    """ Creates/imports the atvm vocabs.
    """
    if context.readDataFile('land.copernicus.content.txt') is None:
        return
    else:
        site = context.getSite()
        atvm = getToolByName(site, ATVOCABULARYTOOL)
        if COUNTRIES_DICTIONARY_ID not in atvm.contentIds():
            hierarchicalVocab = {}
            hierarchicalVocab[(COUNTRIES_DICTIONARY_ID, 'European Countries')] = {}
            createHierarchicalVocabs(atvm, hierarchicalVocab)
            countries = getCountriesDictionary()
            for term in countries.keys():
                vocab = atvm[COUNTRIES_DICTIONARY_ID]
                vocab.invokeFactory('TreeVocabularyTerm', term[0], title=term[1])
                for subterm in countries[term].keys():
                    subvocab = vocab[term[0]]
                    subvocab.invokeFactory('TreeVocabularyTerm', subterm[0], title=subterm[1])
                    subvocab.reindexObject()

                vocab.reindexObject()

        else:
            logger.warn('eea.dataservice countries vocabulary already exist.')
        return