# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/portlet/contextualrecentitems/contextualrecentitems.py
# Compiled at: 2008-02-18 06:58:16
__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 58895 $'
__version__ = '$Revision: 58895 $'[11:-2]
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter, queryAdapter, queryMultiAdapter
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.cache import render_cachekey
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from inquant.portlet.contextualrecentitems import ContextualRecentItemsMessageFactory as _
from inquant.portlet.contextualrecentitems.interfaces import ITypeNameProvider

class IContextualRecentItems(IPortletDataProvider):
    """A portlet which displays recent items of a custom type
    """
    __module__ = __name__
    name = schema.TextLine(title=_('label_contextualrecentitems_portlet', default='Title'), description=_('help_contextualrecentitems_portlet', default='The title of the Portlet. This will appear in the header of the Portlet'), default='Recent Changes', required=False)
    count = schema.Int(title=_('Number of items to display'), description=_('How many items to list.'), required=True, default=5)


class Assignment(base.Assignment):
    __module__ = __name__
    implements(IContextualRecentItems)

    def __init__(self, name='', type='', count=5):
        self.count = count
        self.type = type
        self.name = name

    @property
    def title(self):
        return 'Contextual Recent Items Portlet'


def _render_cachekey(fun, self):
    if self.anonymous:
        raise ram.DontCache()
    return render_cachekey(fun, self)


class Renderer(base.Renderer):
    __module__ = __name__
    _template = ViewPageTemplateFile('contextualrecentitems.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
        self.anonymous = portal_state.anonymous()
        self.portal_url = portal_state.portal_url()
        plone_tools = getMultiAdapter((context, self.request), name='plone_tools')
        self.catalog = plone_tools.catalog()
        self.type = None
        return

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return not self.anonymous and len(self._data())

    @property
    def name(self):
        return self.data.name

    def recent_items(self):
        return self._data()

    def recently_modified_link(self):
        adapter = queryMultiAdapter((self.context, self.request, self.view), ITypeNameProvider)
        if adapter is not None:
            type = adapter.type
            return '%s/@@contextual_recent_modified?type=%s' % (self.portal_url, type)
        else:
            return '%s/recently_modified' % self.portal_url
        return

    @memoize
    def _data(self):
        limit = self.data.count
        query = dict(sort_on='modified', sort_order='reverse', sort_limit=limit)
        adapter = queryMultiAdapter((self.context, self.request, self.view), ITypeNameProvider)
        if adapter:
            type = adapter.type
            query['portal_type'] = type
            self.type = type
        return self.catalog(**query)[:limit]


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(IContextualRecentItems)
    label = _('Add Contextual Recent Items Portlet')
    description = _('This portlet displays recently modified content of a custom Type.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(IContextualRecentItems)
    label = _('Edit Contextual Recent Items Portlet')
    description = _('This portlet displays recently modified content of a custom Type.')