# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/46_47.py
# Compiled at: 2019-05-21 05:08:43
from logging import getLogger
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.utils import getToolByName

def upgrade(context, logger=None):
    if logger is None:
        logger = getLogger('esdrt.content.upgrades.46_47')
    remove_vocabulary(context, logger)
    return


def remove_vocabulary(context, logger):
    pv_tool = getToolByName(context, 'portal_vocabularies')
    pv_vocab = pv_tool.get('crf_code', None)
    vocab_factory = getUtility(IVocabularyFactory, name='esdrt.content.crf_code')
    reg_vocab = vocab_factory(context)
    if compare_vocabs(pv_vocab, reg_vocab, logger):
        pv_tool.manage_delObjects(['crf_code'])
        logger.info('Deleted crf_code vocabulary')
    else:
        logger.info('Registry vocab different from portal_vocabularies.')
    return


def compare_vocabs(pv_vocab, reg_vocab, logger):
    pv_dict = pv_vocab.getVocabularyDict()
    are_the_same = True
    for key, value in pv_dict.items():
        try:
            term = reg_vocab.getTerm(key)
        except LookupError:
            are_the_same = False

        if term.title != value:
            logger.info('%s != %s for %s', term.title, value, key)
            are_the_same = False

    return are_the_same