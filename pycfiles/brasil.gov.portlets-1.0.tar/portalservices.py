# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/controlpanel/portalservices.py
# Compiled at: 2018-10-18 17:35:13
from brasil.gov.portal import _
from plone import api
from plone.app.registry.browser import controlpanel
from plone.i18n.normalizer import idnormalizer
from plone.memoize.view import memoize
from Products.CMFCore.ActionInformation import Action
from Products.CMFCore.ActionInformation import ActionCategory
from Products.CMFCore.interfaces import IAction
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.interface import Interface
import re, time, z3c.form.interfaces
ACTION_CATEGORY = 'portal_services'

class IPortalServicesSettings(Interface):
    u"""Campos dos formulários de inserção e edição do Configlet."""
    pid = schema.TextLine(title=_('id'), required=False)
    title = schema.TextLine(title=_('Titulo do link'), required=True)
    description = schema.Text(title=_('Description'), description=_('Informe a descrição caso seja necessário.'), required=False)
    url_expr = schema.TextLine(title=_('URL'), description=_('Informe o caminho relativo ao portal e começando com uma barra "/" e para URL externa informe http:// ou https://.'), required=True)
    visible = schema.Bool(title=_('Visível'), description=_('Desmarque para ocultar o link.'), default=True)


def get_category():
    """Obtem a categoria do portal_actions"""
    portal_actions = api.portal.get_tool(name='portal_actions')
    category = portal_actions.get(ACTION_CATEGORY, None)
    if not category:
        portal_actions._setObject(ACTION_CATEGORY, ActionCategory(ACTION_CATEGORY))
        return get_category()
    else:
        return category


def url_expression(url):
    u"""Insere a expressão apropriada para a url"""
    if url.find('/') == 0:
        return 'string:${globals_view/navigationRootUrl}%s' % url
    else:
        if url.find('string:') == 0:
            return url
        if re.compile('^(ht|f)tps?\\:', re.I).search(url):
            return 'string:%s' % url
        return 'string:${portal_url}/%s' % url


class PortalServicesSettings(BrowserView):
    """Configlet gereciador dos links adicionados."""
    template = ViewPageTemplateFile('portalservices.pt')

    def __call__(self):
        form = self.request.form
        if form.get('pid', False):
            if form.get('form.button.delete', None) is not None:
                pid = form.get('pid', None)
                if self.delete_item(pid):
                    api.portal.show_message(message=_('Item deleted.'), request=self.request)
                else:
                    api.portal.show_message(message=_('Item not deleted.'), request=self.request)
            elif form.get('form.button.moveup', None) is not None:
                pid = form.get('pid', None)
                if self.move_item(pid, 'move_up'):
                    api.portal.show_message(message=_('Item moved.'), request=self.request)
                else:
                    api.portal.show_message(message=_('Item not moved.'), request=self.request)
            elif form.get('form.button.movedown', None) is not None:
                pid = form.get('pid', None)
                if self.move_item(pid, 'move_down'):
                    api.portal.show_message(message=_('Item moved.'), request=self.request)
                else:
                    api.portal.show_message(message=_('Item not moved.'), request=self.request)
        return self.template()

    @memoize
    def get_items(self):
        items = []
        for item in get_category().objectValues():
            if IAction.providedBy(item):
                items.append(item)

        return items

    def delete_item(self, pid):
        portal_tabs = get_category()
        portal_tabs.manage_delObjects(ids=[pid])
        return True

    def move_item(self, pid, op):
        portal_tabs = get_category()
        if op == 'move_up':
            portal_tabs.moveObjectsUp([pid], 1)
        else:
            portal_tabs.moveObjectsDown([pid], 1)
        return True


class PortalServicesAddForm(form.AddForm):
    u"""Formulário de adicição de action no portal_actions."""
    label = _('Add a link.')
    fields = field.Fields(IPortalServicesSettings)

    def updateWidgets(self):
        super(PortalServicesAddForm, self).updateWidgets()
        self.widgets['pid'].mode = z3c.form.interfaces.HIDDEN_MODE
        self.widgets['visible'].mode = z3c.form.interfaces.HIDDEN_MODE

    def create(self, data):
        id = idnormalizer.normalize(data['title'])
        id += '-' + str(int(time.time()))
        data.pop('pid')
        data['title'] = data['title']
        if data['description']:
            data['description'] = data['description']
        else:
            data['description'] = ''
        data['i18n_domain'] = 'plone'
        data['permissions'] = ('View', )
        data['visible'] = True
        data['url_expr'] = url_expression(data.get('url_expr'))
        action = Action(id, **data)
        return action

    def add(self, action):
        category = get_category()
        category._setObject(action.id, action)
        self.status = _('Item added successfully.')

    def nextURL(self):
        url = self.context.absolute_url()
        url += '/@@portal-services-settings'
        return url


class PortalServicesAddFormPageWrapper(controlpanel.ControlPanelFormWrapper):
    u"""Página de configuração do Portal Padrão"""
    form = PortalServicesAddForm


class PortalServicesEditForm(form.EditForm):
    u"""Formulálio de edição de action no portal_actions."""
    label = _('Edit link')
    schema = IPortalServicesSettings
    fields = field.Fields(IPortalServicesSettings)

    def getContent(self):
        pip = self.request.get('pid', False)
        if not pip:
            self.request.response.redirect(self.nextURL())
        category = get_category()
        item = category.get(pip, None)
        if not item:
            item = dict(pid='', title='', description='', url_expr='', visible=False)
            self.request.response.redirect(self.nextURL())
        else:
            item = dict(pid=item.id and item.id or '', title=item.title and item.title or '', description=item.description and item.description or '', url_expr=item.url_expr and item.url_expr or '', visible=item.visible)
        return item

    def updateWidgets(self):
        super(PortalServicesEditForm, self).updateWidgets()
        self.widgets['pid'].mode = z3c.form.interfaces.HIDDEN_MODE

    @button.buttonAndHandler(_('label_save', default='Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        api.portal.show_message(message=_('Edit successfully'), request=self.request)
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_('label_cancel', default='Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(message=_('Edit cancelled'), request=self.request)
        self.request.response.redirect(self.nextURL())

    def applyChanges(self, data):
        pid = data.pop('pid')
        category = get_category()
        item = category.get(pid, None)
        data['url_expr'] = url_expression(data.get('url_expr'))
        for key in data.keys():
            if key in data:
                data[key] = data[key] and data[key] or ''
                item._setPropValue(key, data[key])

        return

    def nextURL(self):
        url = self.context.absolute_url() + '/@@portal-services-settings'
        return url


class PortalServicesEditFormPageWrapper(controlpanel.ControlPanelFormWrapper):
    u"""Página de configuração do Portal Services"""
    form = PortalServicesEditForm