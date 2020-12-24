# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_controlpanel/kotti_controlpanel/config.py
# Compiled at: 2016-08-21 12:54:46
import colander, deform
from kotti_controlpanel import _
SETTINGS = {}
CONTROL_PANEL_LINKS = {}
slot_names = (
 (
  'left', _('left')),
 (
  'right', _('right')),
 (
  'abovecontent', _('abovecontent')),
 (
  'belowcontent', _('belowcontent')),
 (
  'beforebodyend', _('beforebodyend')))

class SlotSchemaNode(colander.SchemaNode):
    name = 'slot'
    title = _('Direction')
    default = 'left'
    widget = deform.widget.SelectWidget(values=slot_names)


show_in_context = (
 (
  'everywhere', _('Everywhere')),
 (
  'only on root', _('Only on root')),
 (
  'not on root', _('Not on root')),
 (
  'nowhere', _('Nowhere')))

class ShowInContextSchemaNode(colander.SchemaNode):
    name = 'show_in_context'
    title = _('Show in context')
    default = 'everywhere'
    widget = deform.widget.SelectWidget(values=show_in_context)