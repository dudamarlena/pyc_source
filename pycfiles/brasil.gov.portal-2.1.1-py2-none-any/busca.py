# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/busca/busca.py
# Compiled at: 2018-10-18 17:35:13
from Acquisition import aq_base
from Acquisition import aq_inner
from brasil.gov.vcge.dx.interfaces import IVCGEDx
from plone.app.search.browser import Search as PloneSearch
from six.moves.urllib.parse import urlencode
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

class Search(PloneSearch):
    """Customize Plone search form."""

    def skos(self, item):
        """Return the list of VCGE terms on an item."""
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        self.nav_root_url = ps.navigation_root().absolute_url()
        context = aq_base(aq_inner(item))
        if not IVCGEDx.providedBy(context):
            return ()
        name = 'brasil.gov.vcge'
        util = queryUtility(IVocabularyFactory, name)
        vcge = util(context)
        skos = []
        for uri in context.skos:
            title = vcge.by_token[uri].title
            params = urlencode({'skos:list': uri})
            skos.append({'id': uri, 
               'title': title, 
               'url': ('{0}/@@busca?{1}').format(self.nav_root_url, params)})

        return skos

    def rel(self):
        """Formata rel a ser utilizado no href de cada termo
        """
        return 'dc:subject foaf:primaryTopic'