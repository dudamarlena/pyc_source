# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\colors.py
# Compiled at: 2014-04-29 06:05:21
"""
Colors and Backgrounds
http://www.w3.org/TR/1998/REC-CSS2-19980512/colors.html
"""
from trustedhtml.classes import List, Or, Sequence, Complex
from trustedhtml.rules.css.consts import inherit, transparent, none
from trustedhtml.rules.css.syndata import length, percentage, color, uri_image
color = Or(rules=[
 color, inherit])
background_color = Or(rules=[
 color, transparent, inherit])
background_image = Or(rules=[
 uri_image, none, inherit])
background_repeat = List(values=[
 'repeat', 'repeat-x', 'repeat-y', 'no-repeat',
 'inherit'])
background_attachment = List(values=[
 'scroll', 'fixed',
 'inherit'])
background_position_x = Or(rules=[
 List(values=[
  'left', 'center', 'right']),
 percentage,
 length])
background_position_y = Or(rules=[
 List(values=[
  'top', 'center', 'bottom']),
 percentage,
 length])
background_position = Or(rules=[
 Complex(rules=[
  background_position_x,
  background_position_y]),
 inherit])
background = Or(rules=[
 Complex(rules=[
  background_color,
  background_image,
  background_repeat,
  background_attachment,
  background_position_x,
  background_position_y]),
 inherit])