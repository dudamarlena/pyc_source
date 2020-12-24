# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.iconpicker/medialog/iconpicker/browser/tiles.py
# Compiled at: 2019-03-04 06:48:35
from plone import api
from plone.app.tiles.browser.add import DefaultAddForm
from plone.app.tiles.browser.add import DefaultAddView
from plone.app.tiles.browser.edit import DefaultEditForm
from plone.app.tiles.browser.edit import DefaultEditView
from plone.memoize.view import memoize
from plone.supermodel import model
from plone.tiles import Tile
from plone.tiles.data import TransientTileDataManager
from plone.tiles.interfaces import ITileDataManager
from zope import schema
from zope.i18nmessageid import MessageFactory
from plone.autoform.directives import widget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.schema import getFields
from plone.tiles.interfaces import ITileType
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
_ = MessageFactory('medialog.iconpicker')
from medialog.iconpicker.widgets.widget import IconPickerFieldWidget
from medialog.iconpicker.widgets.widget import ColorPickerFieldWidget
from medialog.iconpicker.interfaces import IIconPickerSettings

class IIconTile(model.Schema):
    iconfield = schema.TextLine(title=_('icon', default='Icon'), required=False, description=_('help_icon', default='Choose Icon'))
    widget(iconfield=IconPickerFieldWidget)
    color = schema.TextLine(title=_('color', default='Color'), required=False, description=_('help_color', default='Choose Color'))
    widget(color=ColorPickerFieldWidget)
    title = schema.TextLine(title=_('title', default='Title'), required=False, description=_('help_tittel', default='Title'))
    text = schema.TextLine(title=_('text', default='Text'), required=False, description=_('help_text', default='Text'))
    link = schema.URI(title='Link', required=False)
    css_class = schema.TextLine(title=_('css class', default='CSS class'), required=False, description=_('help_css_class', default='CSS Class'))


class IconTile(Tile):
    """A tile that displays icon and some text"""

    def __init__(self, context, request):
        super(IconTile, self).__init__(context, request)

    @property
    def data(self):
        data = super(IconTile, self).data
        return data

    @property
    def family_css(self):
        iconset = self.iconset()
        if iconset == 'glyphicon':
            return 'glyphicon'
        if iconset == 'mapicon':
            return 'map-icons'
        if iconset == 'typicon':
            return 'typcn'
        if iconset == 'ionicon':
            return 'ionicons'
        if iconset == 'weathericon':
            return 'wi'
        if iconset == 'octicon':
            return 'octicon'
        if iconset == 'elusiveicon':
            return 'el-icon'
        if iconset == 'medialogfont':
            return 'medialogfont'
        if iconset == 'iconpickerfont':
            return 'iconpickerfont'
        if iconset == 'lineawsome':
            return 'linewsome'
        return 'fa'

    def iconset(self):
        """Returns current iconset name This is also used for loading the resources below"""
        return api.portal.get_registry_record('medialog.iconpicker.interfaces.IIconPickerSettings.iconset')


class IPair(model.Schema):
    iconfield = schema.TextLine(title=_('icon', default='Icon'), required=False, description=_('help_icon', default='Choose Icon'))
    widget(iconfield=IconPickerFieldWidget)
    title = schema.TextLine(title=_('title', default='Title'), required=False, description=_('help_tittel', default='Title'))
    text = schema.TextLine(title=_('text', default='Text'), required=False, description=_('help_text', default='Text'))


class IMultiIconTile(model.Schema):
    color = schema.TextLine(title=_('color', default='Color'), required=False, description=_('help_color', default='Choose Color'))
    widget(color=ColorPickerFieldWidget)
    css_class = schema.TextLine(title=_('css class', default='CSS class'), required=False, description=_('help_css_class', default='CSS Class'))
    widget(iconpairs=DataGridFieldFactory)
    iconpairs = schema.List(title=_('icon text_pairs', default='Icon Text pairs'), value_type=DictRow(schema=IPair), required=False)