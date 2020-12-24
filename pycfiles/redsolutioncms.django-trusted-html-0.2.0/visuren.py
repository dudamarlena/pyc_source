# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\visuren.py
# Compiled at: 2014-04-29 06:05:21
"""
Visual formatting model
http://www.w3.org/TR/1998/REC-CSS2-19980512/visuren.html
"""
from trustedhtml.classes import List, Or
from trustedhtml.rules.css.consts import inherit, auto
from trustedhtml.rules.css.syndata import length, percentage, integer
display = List(values=[
 'inline', 'block', 'list-item', 'run-in', 'compact', 'marker', 'table',
 'inline-table', 'table-row-group', 'table-header-group',
 'table-footer-group', 'table-row', 'table-column-group',
 'table-column', 'table-cell', 'table-caption', 'none',
 'inherit'])
position = List(values=[
 'static', 'relative', 'absolute', 'fixed',
 'inherit'])
top = Or(rules=[
 length, percentage, auto, inherit])
float = List(values=[
 'left', 'right', 'none',
 'inherit'])
clear = List(values=[
 'none', 'left', 'right', 'both',
 'inherit'])
z_index = Or(rules=[
 auto, integer, inherit])
direction = List(values=[
 'ltr', 'rtl',
 'inherit'])
unicode_bidi = List(values=[
 'normal', 'embed', 'bidi-override',
 'inherit'])