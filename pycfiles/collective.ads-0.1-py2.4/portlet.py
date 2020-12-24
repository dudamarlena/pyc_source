# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/ads/browser/portlet.py
# Compiled at: 2009-01-02 08:56:18
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_inner, aq_base, aq_parent
from Products.CMFPlone.interfaces import INonStructuralFolder, IBrowserDefault
import random
from DateTime import DateTime
import math
from Products.Archetypes.public import DisplayList

class IAdsPortlet(IPortletDataProvider):
    """A portlet which can render a Ads
    """
    __module__ = __name__
    name = schema.TextLine(title=_('label_title', default='Title'), description=_('help_title', default='The title'), default='', required=False)
    count = schema.Int(title=_('Number of items to display'), description=_('How many items to list.'), required=True, default=5)
    state = schema.Tuple(title=_('Workflow state'), description=_('Items in which workflow state to show.'), default=('published', ), required=True, value_type=schema.Choice(vocabulary='plone.app.vocabularies.WorkflowStates'))


from Products.CMFPlone.utils import log

class Assignment(base.Assignment):
    __module__ = __name__
    implements(IAdsPortlet)

    def __init__(self, name='', count=5, state=('published', )):
        self.count = count
        self.state = state
        self.name = name

    title = _('Ads', default='Ads')


class Renderer(base.Renderer):
    __module__ = __name__

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

    def title(self):
        return self.data.name or ''

    def update(self):
        pass

    def getFilteredBanners(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        state = self.data.state
        count = self.data.count
        banners = catalog(portal_type='Banner', effectiveRange=DateTime(), review_state=state)
        bannerPool = []
        for banner in banners:
            percentage = banner.getPercent
            if percentage != 0:
                percentage = int(math.ceil(percentage / 100))
                if banner.getClicksUsed < banner.getClicks:
                    for i in range(percentage):
                        bannerPool.append(banner)

        if len(bannerPool) > count:
            bannerPool = random.sample(bannerPool, count)
        return bannerPool

    render = ViewPageTemplateFile('templates/adsportlet.pt')


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(IAdsPortlet)
    label = _('Add Ads Portlet')
    description = _('Displays banners in this plone site ')

    def create(self, data):
        return Assignment(name=data.get('name', ''), count=data.get('count', 5), state=data.get('state', ('published', )))


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(IAdsPortlet)
    label = _('Edit Ads Portlet')
    description = _('Displays banners in this Plone sit')