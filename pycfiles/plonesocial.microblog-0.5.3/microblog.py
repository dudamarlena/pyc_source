# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/portlets/microblog.py
# Compiled at: 2013-04-12 05:54:49
from zope.interface import implements
from zope import schema
from zope.formlib import form
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plonesocial.microblog')
from plonesocial.microblog.browser.status import StatusViewlet

class IMicroblogPortlet(IPortletDataProvider):
    """A portlet to render the microblog.
    """
    title = schema.TextLine(title=_('Title'), description=_('A title for this portlet'), required=True, default='Microblog')
    compact = schema.Bool(title=_('Compact rendering'), description=_('Hide portlet header and footer'), default=True)


class Assignment(base.Assignment):
    implements(IMicroblogPortlet)
    title = ''

    def __init__(self, title='Microblog', compact=True):
        self.title = title
        self.compact = compact


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self._statusviewlet = StatusViewlet(context, request, view, manager)
        self._statusviewlet.portlet_data = data

    @property
    def available(self):
        return self._statusviewlet.available

    @property
    def compact(self):
        return self.data.compact

    def update(self):
        self._statusviewlet.update()

    render = ViewPageTemplateFile('microblog.pt')

    def statusform(self):
        return self._statusviewlet.render()


class AddForm(base.AddForm):
    form_fields = form.Fields(IMicroblogPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IMicroblogPortlet)