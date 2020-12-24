# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/controlpanel/portal.py
# Compiled at: 2018-11-30 15:01:51
__doc__ = 'Configuration configlet for IDG.\n\nIt currently includes privacy and header options.\n\nIn the future this configlet should list all IDG options if possible to\navoid having too many configlets.\n'
from brasil.gov.portal import _
from brasil.gov.portal.utils import validate_background
from brasil.gov.portal.utils import validate_list_of_links
from plone.app.registry.browser import controlpanel
from plone.autoform import directives as form
from plone.formwidget.namedfile.widget import NamedFileFieldWidget
from plone.supermodel import model
from zope import schema

class ISettingsPortal(model.Schema):
    u"""Campos do formulário de configuração do Portal Padrão."""
    esconde_autor = schema.Bool(title=_('Hides author'), description=_('Hide information about who created an item.'), default=False, required=False)
    esconde_data = schema.Bool(title=_('Hides publication date'), description=_('Hide information about when an item has been published.'), default=False, required=False)
    model.fieldset('header', label='Header', fields=[
     'expandable_header',
     'background_image',
     'featured_news',
     'more_news',
     'featured_services',
     'more_services',
     'top_subjects'])
    expandable_header = schema.Bool(title=_('Use expandable header?'), description=_('help_expandable_header', default='If enabled, an expandable header will be used instead of the default. A list of search sugestions and hot topics will also be shown, if available.'), default=False)
    form.widget('background_image', NamedFileFieldWidget)
    background_image = schema.ASCII(title=_('title_background_image', default='Background'), description=_('help_background_image', default='An image or video to be used as background of the header. Should be 1440px width and 605px height.'), required=False, constraint=validate_background)
    form.widget('featured_news', cols=25, rows=10)
    featured_news = schema.Tuple(title=_('Notícias em destaque'), description=_('help_featured_news', default=_('You must use "Title|http://example.org" format to fill each line.')), required=False, default=(), value_type=schema.TextLine(), constraint=validate_list_of_links)
    more_news = schema.URI(title=_('Mais notícias'), required=False)
    form.widget('featured_services', cols=25, rows=10)
    featured_services = schema.Tuple(title=_('Serviços em destaque'), description=_('help_featured_services', default=_('You must use "Title|http://example.org" format to fill each line.')), required=False, default=(), value_type=schema.TextLine(), constraint=validate_list_of_links)
    more_services = schema.URI(title=_('Mais serviços'), required=False)
    form.widget('top_subjects', cols=25, rows=10)
    top_subjects = schema.Tuple(title=_('Assuntos em alta'), description=_('help_top_subjects', default=_('You must use "Title|http://example.org" format to fill each line.')), required=False, default=(), value_type=schema.TextLine(), constraint=validate_list_of_links)


class PortalEditForm(controlpanel.RegistryEditForm):
    u"""Formulário de configuração do Portal Padrão."""
    schema = ISettingsPortal
    label = _('e-Government Digital Identity Settings')
    description = _('Settings for e-Government Digital Identity.')


class PortalControlPanel(controlpanel.ControlPanelFormWrapper):
    u"""Página de configuração do Portal Padrão"""
    form = PortalEditForm