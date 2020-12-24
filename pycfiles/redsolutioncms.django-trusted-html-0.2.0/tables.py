# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\tables.py
# Compiled at: 2014-04-29 06:05:21
"""
Tables
http://www.w3.org/TR/1998/REC-CSS2-19980512/tables.html
"""
from trustedhtml.classes import List, Or, Sequence
from trustedhtml.rules.css.consts import inherit
from trustedhtml.rules.css.syndata import length
caption_side = List(values=[
 'top', 'bottom', 'left', 'right',
 'inherit'])
table_layout = List(values=[
 'auto', 'fixed',
 'inherit'])
border_collapse = List(values=[
 'collapse', 'separate',
 'inherit'])
border_spacing_base = Sequence(rule=length, min_split=1, max_split=2)
border_spacing = Or(rules=[
 border_spacing_base, inherit])
empty_cells = List(values=[
 'show', 'hide',
 'inherit'])
speak_header = List(values=[
 'once', 'always',
 'inherit'])