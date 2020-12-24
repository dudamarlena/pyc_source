# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/adam/workspace/virthosts/src/my315ok.portlet.footer/my315ok/portlet/footer/footerportlet.py
# Compiled at: 2010-06-20 04:30:15
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from my315ok.portlet.footer import FooterPortletMessageFactory as _
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

class IFooterPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    text = schema.Text(title=_('Text'), description=_('The text to render'), required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IFooterPortlet)
    text = ''

    def __init__(self, text=''):
        self.text = text

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'Footer portlet'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('footerportlet.pt')


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IFooterPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _('title_add_static_portlet', default='Add static text portlet')
    description = _('description_static_portlet', default='A portlet which can display static HTML text.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(IFooterPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _('title_edit_static_portlet', default='Edit static text portlet')
    description = _('description_static_portlet', default='A portlet which can display static HTML text.')