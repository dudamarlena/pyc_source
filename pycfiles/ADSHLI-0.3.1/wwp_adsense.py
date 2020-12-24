# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/adsense/portlet/wwp_adsense.py
# Compiled at: 2009-07-03 10:07:56
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wwp.adsense.portlet import wwp_adsenseMessageFactory as _

class Iwwp_adsense(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    ad_client = schema.TextLine(title=_('AdSense code'), description=_('Fill with your Google AdSense code \n Code should be appropriate to the dimensions of the portlet'), required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(Iwwp_adsense)

    def __init__(self, ad_client=''):
        self.ad_client = ad_client

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'WWP Adsense'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('wwp_adsense.pt')

    @property
    def js_settings(self):
        data = self.data
        out = []
        out.append('%s' % data.ad_client)
        return ('\n').join(out)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(Iwwp_adsense)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(Iwwp_adsense)