# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/frisi/instances/ritualnetz/src/collective.portlet.localevents/src/collective/portlet/localevents/events.py
# Compiled at: 2015-06-22 16:29:31
from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.localevents import _
from plone import api
from plone.app.portlets import PloneMessageFactory as __
from plone.app.portlets.portlets import base
from plone.app.portlets.portlets.events import Assignment as BaseAssignment
from plone.app.portlets.portlets.events import IEventsPortlet as IBaseEventsPortlet
from plone.app.portlets.portlets.events import Renderer as BaseRenderer
from plone.memoize.instance import memoize
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
POLICY_PORTLET_CONTEXT = 1
POLICY_CURRENT_CONTEXT = 2
policies = SimpleVocabulary([
 SimpleTerm(value=POLICY_PORTLET_CONTEXT, title=_('Context the portlet is assigned on')),
 SimpleTerm(value=POLICY_CURRENT_CONTEXT, title=_('Context the portlet is shown on'))])

class ILocalEventsPortlet(IBaseEventsPortlet):
    title = schema.TextLine(title=_('Title'), required=False)
    policy = schema.Choice(title=_('Search context'), description=_('Define the context in which to search for events'), default=POLICY_PORTLET_CONTEXT, required=True, vocabulary=policies)


class Assignment(BaseAssignment):
    implements(ILocalEventsPortlet)
    portletHeading = None
    policy = POLICY_PORTLET_CONTEXT

    def __init__(self, count=5, state=('published', ), policy=POLICY_PORTLET_CONTEXT, title=None):
        self.count = count
        self.state = state
        self.policy = policy
        self.portletHeading = title

    @property
    def title(self):
        return self.portletHeading or __('Events')


class Renderer(BaseRenderer):
    _template = ViewPageTemplateFile('events.pt')

    def title(self):
        return self.data.portletHeading or __('box_events', default='Upcoming Events')

    def prev_events_link(self):
        return

    def assignment_context(self):
        """return the context the portlet has been assigned on
        """
        assignment_context_path = self.__portlet_metadata__['key']
        return self.context.restrictedTraverse(assignment_context_path)

    def current_context(self):
        """return context the portlet is currently shown on.
        return the folder in case we're on a default page"""
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        return context_state.canonical_object()

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool('portal_catalog')
        calendar_details = api.portal.get_tool('portal_calendar')
        limit = self.data.count
        state = self.data.state
        if self.data.policy == POLICY_PORTLET_CONTEXT:
            search_context = self.assignment_context()
        else:
            search_context = self.current_context()
        path = ('/').join(search_context.getPhysicalPath())
        return catalog(portal_type=calendar_details.calendar_types, review_state=state, end={'query': DateTime(), 'range': 'min'}, path=path, sort_on='start', sort_limit=limit)[:limit]


class AddForm(base.AddForm):
    form_fields = form.Fields(ILocalEventsPortlet)
    label = __('Add Events Portlet')
    description = __('This portlet lists upcoming Events.')

    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published', )), policy=data.get('policy', POLICY_PORTLET_CONTEXT), title=data.get('title', None))


class EditForm(base.EditForm):
    form_fields = form.Fields(ILocalEventsPortlet)
    label = __('Edit Events Portlet')
    description = __('This portlet lists upcoming Events.')