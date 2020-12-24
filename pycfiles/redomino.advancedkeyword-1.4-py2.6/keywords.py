# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/browser/keywords.py
# Compiled at: 2013-05-08 04:41:18
from zope.publisher.interfaces import NotFound
from zope.publisher.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import queryUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from plone.i18n.normalizer.interfaces import IIDNormalizer
from redomino.advancedkeyword.config import KEYWORD_SEPARATOR
from redomino.advancedkeyword.browser.keywordmapcontrolpanel import IKeywordMapSchema

def cutKeywords(kw):
    """if prefix = redomino.test1.test2 it yields
       - redomino
       - redomino.test1
       - redomino.test1.test2"""
    l = kw.split(KEYWORD_SEPARATOR)
    out = []
    for k in l:
        out.append(k)
        yield ('.').join(out)


class KWGenerator(BrowserView):
    """Keyword tree generator baseclass"""

    def get_all_kw(self):
        raise NotImplementedError

    def get_selected_kw(self):
        raise NotImplementedError

    def _getKWTree(self):
        out = {}
        for item in self.get_all_kw():
            currentdict = out
            for kw in item.split(KEYWORD_SEPARATOR):
                currentdict = currentdict.setdefault(kw, {})

        return out

    def __call__(self):
        return self._getTree(self._getKWTree())

    def _is_selected(self, prefix):
        for kw in self.get_selected_kw():
            for k in cutKeywords(kw):
                if k == prefix:
                    return True

        return False

    @memoize
    def getIdNormalizer(self):
        return queryUtility(IIDNormalizer)

    def _getTree(self, d, prefix=None):
        if not d:
            return []
        idnormalizer = self.getIdNormalizer()
        out = []
        keys = sorted(d.keys(), key=lambda s: s.lower())
        for k in keys:
            newprefix = prefix and KEYWORD_SEPARATOR.join([prefix, k]) or k
            children = self._getTree(d[k], newprefix)
            out.append({'full_keyword': newprefix, 'keyword': k, 
               'children': children, 
               'selected': self._is_selected(newprefix), 
               'is_folder': bool(len(children)), 
               'id': idnormalizer.normalize(newprefix)})

        return out


class KeywordsMapGenerator(KWGenerator):
    """Keyword tree generator for Keyword Map

       - all the subjects
       - I get subjects from the request (sometimes it doesn't matter)
    """

    def get_all_kw(self):
        catalog = getMultiAdapter((self.context, self.context.REQUEST), name='plone_tools').catalog()
        return catalog.uniqueValuesFor('Subject')

    @memoize
    def get_selected_kw(self):
        return self.request.form.get('Subject', [])


class KeywordsWidgetGenerator(KWGenerator):
    """Keyword tree generator for Keyword widget

       - all the subjects
       - the subject in the context
    """

    def get_all_kw(self):
        field = self.context.getField('subject')
        return self.context.collectKeywords(field.getName(), field.accessor, field.widget.vocab_source)

    @memoize
    def get_selected_kw(self):
        return self.context.Subject()

    def unicodeset(self, values):
        unicodeEncode = self.context.unicodeEncode
        return set([ unicodeEncode(v) for v in values ])


class KeywordsMap(BrowserView):
    """ A keyword maps of the whole site """
    template = ViewPageTemplateFile('templates/keywordmap.pt')

    def getTree(self):
        gen = getMultiAdapter((self.context, self.request), name='keywordsmapgenerator')
        return gen()

    def __call__(self):
        """Checks if the sitemap feature is enable and returns it."""
        portal = getMultiAdapter((self.context, self.request), name='plone_portal_state').portal()
        if not IKeywordMapSchema(portal).keywordmapenabled:
            raise NotFound(self.context, 'keywordsmap', self.request)
        return self.template()