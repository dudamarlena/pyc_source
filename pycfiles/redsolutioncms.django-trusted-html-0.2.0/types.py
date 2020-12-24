# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\html\types.py
# Compiled at: 2014-04-29 06:05:21
"""
Basic HTML data types
http://www.w3.org/TR/REC-html40/types.html
"""
from trustedhtml.classes import String, RegExp, Uri, No, Sequence, Style
from trustedhtml.rules.html.grammar import grammar
from trustedhtml.rules import css
idref = name = RegExp(regexp='(%(name)s)$' % grammar)
name_required = RegExp(regexp='(%(name)s)$' % grammar, element_exception=True)
idrefs = RegExp(regexp='(%(name)s(%(w)s%(name)s)*)$' % grammar)
idrefs_comma = RegExp(regexp='(%(name)s(%(w)s,%(w)s%(name)s)*)$' % grammar)
number = RegExp(regexp='(%(number)s)$' % grammar)
number_required = RegExp(regexp='(%(number)s)$' % grammar, element_exception=True)
positive_number = RegExp(regexp='(%(positive-number)s)$' % grammar)
text = String()
text_required = String(element_exception=True)
text_default = String(default='')
uri = Uri()
uri_required = Uri(element_exception=True)
uri_image = Uri(type=Uri.IMAGE)
uri_image_required = Uri(type=Uri.IMAGE, element_exception=True)
uri_object = Uri(type=Uri.OBJECT)
uris = Sequence(rule=Uri())
color = RegExp(regexp='(%(color)s)$' % grammar)
pixels = RegExp(regexp='(%(number)s)$' % grammar)
length = RegExp(regexp='(%(length)s)$' % grammar)
multi_length = RegExp(regexp='(%(multi-length)s)$' % grammar)
multi_lengths = RegExp(regexp='(%(multi-length)s(%(w)s,%(w)s%(multi-length)s)*)$' % grammar)
length_required = RegExp(regexp='(%(length)s)$' % grammar, element_exception=True)
coords = RegExp(regexp='(%(length)s(%(w)s,%(w)s%(length)s)(%(w)s,%(w)s%(length)s)+)$' % grammar)
content_type = RegExp(regexp='(%(content-type)s)$' % grammar)
content_types = RegExp(regexp='(%(content-type)s(%(w)s,%(w)s%(content-type)s)*)$' % grammar)
content_type_required = RegExp(regexp='(%(content-type)s)$' % grammar, element_exception=True)
language_code = RegExp(regexp='(%(language-code)s)$' % grammar)
charset = RegExp(regexp='(%(charset)s)$' % grammar)
charsets = RegExp(regexp='(%(charset)s(%(w)s,?%(w)s%(charset)s)*)$' % grammar)
character = RegExp(regexp='(.)$')
datetime = RegExp(regexp='(%(datetime)s)$' % grammar)
link_types = RegExp(regexp='(%(link-types)s)$' % grammar)
media_descs = Sequence(regexp='\\s*,\\s*', join_string=',', rule=RegExp(regexp='(%(media-desc)s)' % grammar))
style_sheet = css.full
frame_target = RegExp(regexp='(%(frame-target)s)$' % grammar)
script = No()