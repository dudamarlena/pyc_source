# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/googleapps/portlets/googlecalendarportlet.py
# Compiled at: 2009-08-12 23:02:33
from zope.interface import Interface
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.schema import vocabulary as _vocabulary
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.googleapps import portletMessageFactory as _

class IGoogleCalendarPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    header = schema.TextLine(title=_('Portlet header'), description=_('Title of the rendered portlet'), required=True, default=_('My Google Calendar'))
    calendars = schema.TextLine(title=_('Visible Calendars'), description=_("Specify which calendars you'd like as a comma-separated list of addresses. Making no selection will show all calendars by default."), required=False)
    show_minicalendar = schema.Bool(title=_('Show mini calendar?'), description=_('If enabled, a mini-calendar will be displayed at the top.'), required=True, default=False)
    show_emptydays = schema.Bool(title=_('Show days with no events?'), description=_('If enabled, your list of upcoming events will contain days with no events.'), required=True, default=False)
    show_expiredevents = schema.Bool(title=_('Show past events?'), description=_('If enabled, your list of upcoming events will show events from the past.'), required=True, default=True)
    hosted_domain = schema.TextLine(title=_('Hosted domain to access'), description=_("If specified, this will be the domain account that will be accessed (for example, 'university.edu.au').  If not specifed, you will access a regular Google account."), required=False, default=_(''))
    secure_connection = schema.Bool(title=_('Secure connection?'), description=_('If enabled, use the HTTPS protocol (where possible).'), required=True, default=True)
    portlet_height = schema.TextLine(title=_('Portlet height'), description=_('If specified, this will be the height of the portlet (in pixels or percent).'), required=False, default=_(''))
    portlet_width = schema.TextLine(title=_('Portlet width'), description=_('If specified, this will be the width of the portlet (in pixels or percent).'), required=False, default=_(''))


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IGoogleCalendarPortlet)
    header = 'My Google Calendar'
    calendars = None
    show_minicalendar = False
    show_emptydays = False
    show_expiredevents = True
    hosted_domain = ''
    secure_connection = True
    portlet_height = '160'
    portlet_width = '100%'

    def __init__(self, header='My Google Calendar', calendars=None, show_minicalendar=False, show_emptydays=False, show_expiredevents=True, hosted_domain='', secure_connection=True, portlet_height='160', portlet_width='100%'):
        self.header = header
        self.calendars = calendars
        self.show_minicalendar = show_minicalendar
        self.show_emptydays = show_emptydays
        self.show_expiredevents = show_expiredevents
        self.hosted_domain = hosted_domain
        self.secure_connection = secure_connection
        self.portlet_height = portlet_height
        self.portlet_width = portlet_width

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('googlecalendarportlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @memoize
    def google_calendar_iframe_url(self):
        url = 'http' + (self.data.secure_connection and 's' or '') + '://www.google.com/calendar'
        if self.data.hosted_domain:
            url += '/hosted/' + self.data.hosted_domain
        url += '/mgadget?'
        if self.data.calendars:
            url += 'up_calendarFeeds=(' + self.data.calendars + ')'
        url += '&up_showDatepicker=' + (self.data.show_minicalendar and 'true' or 'false')
        url += '&up_showEmptyDays=' + (self.data.show_emptydays and '1' or '0')
        url += '&up_showExpiredEvents=' + (self.data.show_expiredevents and 'true' or 'false')
        return url

    def google_url(self):
        url = 'http' + (self.data.secure_connection and 's' or '') + '://www.google.com/calendar'
        if self.data.hosted_domain:
            url += '/hosted/' + self.data.hosted_domain
        url += '/render'
        return url


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IGoogleCalendarPortlet)

    def create(self, data):
        print self.form_fields.__dict__
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(IGoogleCalendarPortlet)
    label = _('Edit Google Calendar Portlet')
    description = _('A portlet for Plone that displays content from your Google Calendar.')