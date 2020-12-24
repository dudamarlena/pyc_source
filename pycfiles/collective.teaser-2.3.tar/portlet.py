# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/browser/portlet.py
# Compiled at: 2013-03-13 08:34:51
import uuid
from node.utils import instance_property
from zope.component import getUtility, getMultiAdapter
from zope.interface import implements
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import get_language
from plone.app.portlets.portlets import base
from plone.app.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from Acquisition import aq_inner, aq_parent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.teaser.config import DEFAULT_IMPORTANCE
from collective.teaser.browser.common import get_teasers
_ = MessageFactory('collective.teaser')

def render_cachekey(fun, self):
    """
    Based on render_cachekey from plone.app.portlets.cache, without the
    fingerprint based on the portlet's catalog brains.

    Generates a key based on:

    * Portal URL
    * Negotiated language
    * Anonymous user flag
    * Portlet manager
    * Assignment

    """
    context = aq_inner(self.context)
    anonymous = getToolByName(context, 'portal_membership').isAnonymousUser()
    return ('').join((
     getToolByName(aq_inner(self.context), 'portal_url')(),
     get_language(aq_inner(self.context), self.request),
     str(anonymous),
     self.manager.__name__,
     self.data.__name__))


def get_portlet_assingment(context, uid):
    context_orgin = context
    for name in ['plone.leftcolumn', 'plone.rightcolumn',
     'collective.teaser.portletmanager']:
        manager = getUtility(IPortletManager, name=name)
        for category in manager.values():
            for group in category.values():
                for assignment in group.values():
                    if ITeaserPortlet.providedBy(assignment):
                        if uid == str(assignment.uid):
                            return assignment

        context = aq_inner(context_orgin)
        while True:
            try:
                assignment_mapping = getMultiAdapter((context, manager), IPortletAssignmentMapping)
            except:
                return

            for assignment in assignment_mapping.values():
                if ITeaserPortlet.providedBy(assignment):
                    if uid == str(assignment.uid):
                        return assignment

            if IPloneSiteRoot.providedBy(context):
                break
            context = aq_parent(aq_inner(context))

    raise KeyError("Portlet assignment for uid '%s' not found." % uid)


class TeaserRenderer(object):
    template = PageTemplateFile('teaser.pt')

    def __init__(self, context, data, request):
        self.context = context
        self.data = data
        self.request = request

    def __call__(self):
        return self.template(options=self)

    @property
    def display_columns(self):
        return int(self.data.display_columns)

    @property
    def table_rows(self):
        count = len(self.teasers)
        if count == 1:
            return count
        rows = count / 2
        if count % 2 != 0:
            rows += 1
        return rows

    @instance_property
    def teasers(self):
        return get_teasers(self.context, self.data, self.request)


class AjaxTeaser(BrowserView):

    def __call__(self):
        return TeaserRenderer(self.context, self.data, self.request)()

    @property
    def data(self):
        return get_portlet_assingment(self.context, self.request.get('uid'))


display_columns = SimpleVocabulary([
 SimpleTerm(value='1', title=_('One')),
 SimpleTerm(value='2', title=_('Two'))])

class ITeaserPortlet(IPortletDataProvider):
    header = schema.TextLine(title=_('Portlet header'), description=_('Title of the rendered portlet'), required=False)
    display_columns = schema.Choice(title=_('portlet_label_display_columns', default='Number of columns'), description=_('portlet_help_display_columns', default='Select number of columns to display'), vocabulary=display_columns, default='1', required=True)
    importance_levels = schema.Tuple(title=_('portlet_label_importance_levels', default='Importance Levels'), description=_('portlet_help_importance_levels', default='Select which importance levels the portlet should show.'), default=(
     DEFAULT_IMPORTANCE,), required=True, value_type=schema.Choice(vocabulary='collective.teaser.ImportanceVocabulary'))
    keywords_filter = schema.Tuple(title=_('portlet_label_keywords_filter', default='Keywords Filter'), description=_('portlet_help_keywords_filter', default='Select which teasers with specific keywords should be shown. Select none to order to show any teasers.'), default=None, required=False, value_type=schema.Choice(vocabulary='plone.app.vocabularies.Keywords'))
    teaser_scale = schema.Choice(title=_('portlet_label_image_scale', default='Image Scale'), description=_('portlet_help_image_scale', default='Select, which image scale should be used for the portlet.'), required=True, default=None, vocabulary='collective.teaser.ImageScaleVocabulary')
    num_teasers = schema.Int(title=_('portlet_label_num_teasers', default='Number of teasers'), description=_('portlet_help_num_teasers', default='Define the maximum number of teasers, which are displayed in this portlet'), default=1, required=True)
    ajaxified = schema.Bool(title=_('portlet_label_ajaxified', default='Load Teasers via AJAX?'), description=_('portlet_help_ajaxified', default='Whether teaser is loaded deferred via ajax or directly.'), default=True, required=False)
    show_title = schema.Bool(title=_('portlet_label_show_title', default='Show title'), description=_('portlet_help_show_title', default='Show the title of the teaser.'), default=True, required=False)
    show_description = schema.Bool(title=_('portlet_label_show_description', default='Show description'), description=_('portlet_help_show_description', default='Show the description of the teaser as text ' + 'below the image.'), default=False, required=False)
    search_base = schema.Choice(title=_('portlet_label_search_base', default='Search base'), description=_('portlet_help_search_base', default='Select teaser search base folder'), source=SearchableTextSourceBinder({'is_folderish': True}, default_query='path:'), required=False)


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('teaser_portlet.pt')

    @memoize
    def renderer(self):
        return TeaserRenderer(self.context, self.data, self.request)

    @property
    def display(self):
        return bool(self.renderer().teasers)

    @property
    def rendered_teasers(self):
        return self.renderer()

    def has_header(self):
        return bool(self.data.header)


class Assignment(base.Assignment):
    implements(ITeaserPortlet)
    show_description = False
    keywords_filter = None
    search_base = None

    def __init__(self, importance_levels=None, keywords_filter=None, teaser_scale=None, num_teasers=1, ajaxified=True, show_title=True, show_description=False, search_base=None, header='', display_columns='1'):
        self._header = header
        self._display_columns = display_columns
        self.importance_levels = importance_levels
        self.keywords_filter = keywords_filter
        self.teaser_scale = teaser_scale
        self.num_teasers = num_teasers
        self.ajaxified = ajaxified
        self.show_title = show_title
        self.show_description = show_description
        self.search_base = search_base
        self.uid = uuid.uuid4()

    def _get_header(self):
        if not hasattr(self, '_header'):
            self._header = ''
        return self._header

    def _set_header(self, header):
        self._header = header

    header = property(_get_header, _set_header)

    def _get_display_columns(self):
        if not hasattr(self, '_display_columns'):
            self._display_columns = '1'
        return self._display_columns

    def _set_display_columns(self, columns):
        self._display_columns = columns

    display_columns = property(_get_display_columns, _set_display_columns)

    @property
    def title(self):
        return self.header or _('portlet_teaser_title', default='Teaser')


class AddForm(base.AddForm):
    form_fields = form.Fields(ITeaserPortlet)
    label = _('portlet_label_add', default='Add portlet to show teasers.')
    description = _('portlet_help_add', default='This portlet shows teasers.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ITeaserPortlet)
    label = _('portlet_label_add', default='Add portlet to show teasers.')
    description = _('portlet_help_add', default='This portlet shows teasers.')