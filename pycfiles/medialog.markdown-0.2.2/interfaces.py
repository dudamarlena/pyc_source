# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.markdown/medialog/markdown/interfaces.py
# Compiled at: 2018-02-07 06:06:26
from z3c.form import interfaces
from zope import schema
from zope.interface import alsoProvides
from plone.directives import form
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('medialog.markdown')

class IButtonPair(form.Schema):
    name = schema.ASCIILine(title=_('name', 'Name'), required=False, default='Important')
    icon = schema.ASCIILine(title=_('icon', 'Icon'), required=False, default='fa-exclamation')
    buttontext = schema.TextLine(title=_('buttontext', 'buttontext'), required=False, default='!!! important "Important"\\n     \x08')


class IMarkdownSettings(form.Schema):
    """Adds settings to medialog.controlpanel
    """
    form.fieldset('markdown', label=_('Markdown settings'), fields=[
     'button_pairs',
     'live_preview'])
    live_preview = schema.Bool(title=_('Live preview', 'live preview'))
    form.widget(button_pairs=DataGridFieldFactory)
    button_pairs = schema.List(title=_('button_pairs', default='Ekstra buttons'), value_type=DictRow(schema=IButtonPair))


alsoProvides(IMarkdownSettings, IMedialogControlpanelSettingsProvider)