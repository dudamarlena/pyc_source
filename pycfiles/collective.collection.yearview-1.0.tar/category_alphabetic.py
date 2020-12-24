# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/collection/alphabetic/browser/category_alphabetic.py
# Compiled at: 2009-06-10 15:31:30
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from collective.collection.alphabetic.browser import topic_alphabetic
from collective.collection.alphabetic.browser.topic_alphabetic import TopicAlphabeticView

class CategoryAlphabeticView(TopicAlphabeticView):
    __module__ = __name__
    template = ViewPageTemplateFile('category_alphabetic_view.pt')

    def __call__(self):
        return self.template()

    def title_url_dictionary_lists(self):
        context = aq_inner(self.context)
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        url = portal_state.portal_url()
        qc = self.queryCatalog()
        character = self.request.get('character', None)
        results = []
        if character:
            uni_character = unicode(character)
            for item in qc:
                category = item.Subject
                if category != ():
                    for c in category:
                        category_url = '%s/search?Subject:list=%s' % (url, c)
                        first_character = unicode(c)[0]
                        if (first_character == uni_character or first_character == uni_character.lower()) and (('title', c), ('url', category_url)) not in results:
                            results.append((('title', c), ('url', category_url)))

            results.sort()
            return [ dict(item) for item in results ]
        else:
            return
        return

    def has_contents(self, character):
        """Return True if there are any contents for the category character."""
        qc = self.queryCatalog()
        category_tuple = [ item.Subject for item in qc ]
        results = []
        for subject in category_tuple:
            for c in subject:
                if c not in results:
                    results.append(c)

        contents = [ c for c in results if unicode(c)[0] == character or unicode(c)[0] == character.lower() ]
        if contents != []:
            return True
        else:
            return False