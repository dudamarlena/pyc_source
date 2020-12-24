# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/skin/search.py
# Compiled at: 2012-06-26 16:39:45
__docformat__ = 'restructuredtext'
from hurry.query.interfaces import IQuery
from zope.intid.interfaces import IIntIds
from zope.session.interfaces import ISession
from ztfy.blog.interfaces.category import ICategorizedContent
from ztfy.blog.interfaces.topic import ITopic
from ztfy.workflow.interfaces import IWorkflowContent
from hurry.query import And
from hurry.query.set import AnyOf
from hurry.query.value import Eq
from zope.component import getUtility
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.skin.page import TemplateBasedPage
from ztfy.utils.catalog.index import Text
from ztfy.utils.traversing import getParent
SITE_MANAGER_SESSION_ID = 'ztfy.gallery.site.search'

class SiteManagerSearchView(TemplateBasedPage):
    """Site manager search page"""

    def __call__(self):
        form = self.request.form
        if 'page' in form:
            session = ISession(self.request)[SITE_MANAGER_SESSION_ID]
            self.search_text = search_text = session.get('search_text', '')
            self.search_tag = search_tag = session.get('search_tag', '') or None
        else:
            self.search_text = search_text = form.get('search_text', '').strip()
            self.search_tag = search_tag = form.get('search_tag', '') or None
        if not search_text:
            if not search_tag:
                self.request.response.redirect(absoluteURL(self.context, self.request))
                return ''
            else:
                intids = getUtility(IIntIds)
                category = intids.queryObject(search_tag)
                self.request.response.redirect(absoluteURL(category, self.request))
                return ''

        return super(SiteManagerSearchView, self).__call__()

    def update(self):
        super(SiteManagerSearchView, self).update()
        query = getUtility(IQuery)
        params = []
        params.append(Text(('Catalog', 'image_title'), {'query': (' ').join('%s*' % m for m in self.search_text.split()), 'autoexpand': 'on_miss', 
           'ranking': True}))
        topics = {}
        [ topics.setdefault(getParent(image, ITopic), []).append(image) for image in query.searchResults(And(*params))
        ]
        if self.search_tag:
            for topic in topics.keys()[:]:
                ids = ICategorizedContent(topic).categories_ids
                if ids and self.search_tag not in ids:
                    del topics[topic]

        params = []
        params.append(Eq(('Catalog', 'content_type'), 'ITopic'))
        params.append(Text(('Catalog', 'title'), {'query': (' ').join('%s*' % m for m in self.search_text.split()), 'autoexpand': 'on_miss', 
           'ranking': True}))
        if self.search_tag:
            intids = getUtility(IIntIds)
            self.category = intids.queryObject(self.search_tag)
            params.append(AnyOf(('Catalog', 'categories'), (self.search_tag,)))
        [ topics.setdefault(topic, []) for topic in query.searchResults(And(*params)) ]
        for topic in topics.keys()[:]:
            if not IWorkflowContent(topic).isVisible():
                del topics[topic]

        results = sorted(((topic, topics[topic]) for topic in topics), key=lambda x: IWorkflowContent(x[0]).publication_effective_date, reverse=True)
        session = ISession(self.request)[SITE_MANAGER_SESSION_ID]
        session['search_text'] = self.search_text
        session['search_tag'] = self.search_tag
        page = int(self.request.form.get('page', 0))
        page_length = 10
        first = page_length * page
        last = first + page_length - 1
        pages = len(results) / page_length
        if len(results) % page_length:
            pages += 1
        self.results = {'results': results[first:last + 1], 'pages': pages, 
           'first': first, 
           'last': last, 
           'has_prev': page > 0, 
           'has_next': last < len(results) - 1}