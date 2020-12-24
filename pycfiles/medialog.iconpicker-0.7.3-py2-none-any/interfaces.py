# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.iconpicker/medialog/iconpicker/interfaces.py
# Compiled at: 2019-03-04 06:48:35
from z3c.form import interfaces
from zope import schema
from zope.interface import alsoProvides
from plone.supermodel import model
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('medialog.iconpicker')

class IIconPickerSettings(model.Schema):
    """Adds settings to medialog.controlpanel
    https://erikflowers.github.io/weather-icons/
        http://www.typicons.com/
        https://octicons.github.com/
        http://ionicons.com/
        http://elusiveicons.com/cheatsheet/
        https://fortawesome.github.io/Font-Awesome/icons/
        http://map-icons.com/
    """
    model.fieldset('iconpicker', label=_('Iconpicker settings'), fields=[
     'iconset',
     'cols',
     'rows',
     'placement',
     'loadbootstrap'])
    iconset = schema.Choice(title=_('label_iconset', default='Iconset'), description=_('help_iconset', default='Choose iconset to be used for iconpicker.Some links:\n        <a href="https://erikflowers.github.io/weather-icons/">Weather-icons</a> •\n        <a href="http://www.typicons.com">Typicons</a> •\n        <a href="https://octicons.github.com/">Octicons</a> •\n        <a href="http://ionicons.com/">Ionicons</a>  •\n        <a href="">http://elusiveicons.com/cheatsheet/</a>  •\n        <a href="https://fortawesome.github.io/Font-Awesome/icons/">Font Awsome</a>  •\n        <a href="http://map-icons.com/">map-icons</a>\n        '), values=[
     'glyphicon', 'ionicon', 'fontawesome', 'weathericon', 'mapicon', 'octicon', 'typicon', 'elusiveicon', 'medialogfont', 'iconpickerfont', 'lineawesome'])
    loadbootstrap = schema.Bool(title=_('label_loadbootstrap', default='Load Bootstrap'), description=_('help_loadbootstrap', default='Loads ++resource++collective.js.bootstrap/js/bootstrap.min.js. <br/>\n            You probably want to do this in your diazo theme instead.'))
    cols = schema.Int(title=_('label_columns', default='Columns'))
    rows = schema.Int(title=_('label_rows', default='Rows'))
    placement = schema.Choice(title=_('label_placement', default='Placement'), values=[
     'left', 'top', 'bottom', 'right'])


alsoProvides(IIconPickerSettings, IMedialogControlpanelSettingsProvider)