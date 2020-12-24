# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/replaceKeywordsWidget.py
# Compiled at: 2008-10-06 10:31:07
from Products.CMFCore.utils import getToolByName
from browser.archetypes import IncrementalSearchSelectWidget
from Products.Archetypes.Widget import KeywordWidget

def replace_keywords_widget_at_metadata_page(out):
    print >> out, 'Replacing keywords widget to incremental search widget at metadata page...'
    from Products.ATContentTypes.content.document import ATDocument
    ATDocument('widget-temp-document').schema['subject'].widget = IncrementalSearchSelectWidget(label='Keywords', label_msgid='label_keywords', description_msgid='help_keyword', i18n_domain='plone')
    print >> out, 'Replaced.'


def replace_keywords_widget_to_original_at_metadata_page(out):
    print >> out, 'Replacing keywords widget to original one at metadata page...'
    from Products.ATContentTypes.content.document import ATDocument
    ATDocument('widget-temp-document').schema['subject'].widget = KeywordWidget(label='Keywords', label_msgid='label_keywords', description_msgid='help_keyword', i18n_domain='plone')
    print >> out, 'Replaced.'