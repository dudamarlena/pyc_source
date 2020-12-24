# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\ui.py
# Compiled at: 2014-04-29 06:05:21
"""
User interface
http://www.w3.org/TR/1998/REC-CSS2-19980512/ui.html
"""
from trustedhtml.classes import List, Or, Sequence, Complex
from trustedhtml.rules.css.consts import inherit
from trustedhtml.rules.css.syndata import color, uri_image
from trustedhtml.rules.css.box import border_width_base, border_style_base
cursor_base = Or(rules=[
 List(values=[
  'auto', 'crosshair', 'default', 'pointer', 'move', 'e-resize', 'ne-resize',
  'nw-resize', 'n-resize', 'se-resize', 'sw-resize', 's-resize', 'w-resize',
  'text', 'wait', 'help']),
 uri_image])
cursor = Or(rules=[
 Sequence(rule=cursor_base, regexp='\\s,\\s', join_string=','),
 inherit])
outline_width = Or(rules=[
 border_width_base, inherit])
outline_style = Or(rules=[
 border_style_base, inherit])
outline_color_base = Or(rules=[
 color,
 List(values=[
  'invert'])])
outline_color = Or(rules=[
 outline_color_base, inherit])
outline = Or(rules=[
 Complex(rules=[
  border_width_base,
  border_style_base,
  outline_color_base]),
 inherit])