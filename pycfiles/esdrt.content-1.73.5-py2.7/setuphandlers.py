# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/setuphandlers.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
VOCABULARIES = [
 {'id': 'eea_member_states', 'title': 'EEA Member States', 
    'filename': 'eea_member_states.csv'},
 {'id': 'ghg_source_category', 'title': 'CRF category group', 
    'filename': 'ghg_source_category.csv'},
 {'id': 'ghg_source_sectors', 'title': 'CRF Sector', 
    'filename': 'ghg_source_sectors.csv'},
 {'id': 'crf_code', 'title': 'CRF category codes', 
    'filename': 'crf_code.csv'},
 {'id': 'fuel', 'title': 'Fuel', 
    'filename': 'fuel.csv'},
 {'id': 'gas', 'title': 'Gas', 
    'filename': 'gas.csv'},
 {'id': 'highlight', 'title': 'Highligt', 
    'filename': 'highlight.csv'},
 {'id': 'parameter', 'title': 'Parameter', 
    'filename': 'parameter.csv'},
 {'id': 'conclusion_reasons', 'title': 'Conclusion Reasons', 
    'filename': 'conclusion_reasons.csv'},
 {'id': 'conclusion_phase2_reasons', 'title': 'Conclusion Phase2 Reasons', 
    'filename': 'conclusion_phase2_reasons.csv'}]

def create_vocabulary(context, vocabname, vocabtitle, importfilename=None, profile=None):
    _ = context.invokeFactory(id=vocabname, title=vocabtitle, type_name='SimpleVocabulary')
    vocabulary = context.getVocabularyByName(vocabname)
    wtool = getToolByName(context, 'portal_workflow')
    wtool.doActionFor(vocabulary, 'publish')
    from logging import getLogger
    log = getLogger('create_vocabulary')
    log.info('Created %s vocabulary' % vocabname)
    if importfilename is not None:
        data = profile.readDataFile(importfilename, subdir='esdrtvocabularies')
        vocabulary.importCSV(data)
    log.info('done')
    return


def prepareVocabularies(context, profile):
    """ initial population of vocabularies """
    atvm = getToolByName(context, 'portal_vocabularies')
    for vocabulary in VOCABULARIES:
        vocab = atvm.getVocabularyByName(vocabulary.get('id'))
        if vocab is None:
            create_vocabulary(atvm, vocabulary.get('id'), vocabulary.get('title'), vocabulary.get('filename', None), profile)

    return


def enable_atd_spellchecker(portal):
    tinymce = getToolByName(portal, 'portal_tinymce')
    tinymce.libraries_spellchecker_choice = 'AtD'
    tinymce.libraries_atd_service_url = 'service.afterthedeadline.com'


def setupVarious(context):
    """ various import steps for esdrt.content """
    portal = context.getSite()
    if context.readDataFile('esdrt.content_various.txt') is None:
        return
    else:
        prepareVocabularies(portal, context)
        enable_atd_spellchecker(portal)
        return