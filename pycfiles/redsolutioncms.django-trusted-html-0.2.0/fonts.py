# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\fonts.py
# Compiled at: 2014-04-29 06:05:21
"""
Colors and Backgrounds
http://www.w3.org/TR/1998/REC-CSS2-19980512/fonts.html
"""
from trustedhtml.classes import List, RegExp, Or, Sequence, Complex
from trustedhtml.rules.css.consts import inherit, none
from trustedhtml.rules.css.grammar import grammar
from trustedhtml.rules.css.syndata import positive_number, positive_length, positive_percentage
family_name = RegExp(regexp='(([!#$%%&(-~]|\\\\%(nl)s|%(nonascii)s|%(escape)s)*|%(string1)s|%(string2)s)$' % grammar)
generic_family = List(values=[
 'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'])
font_family = Or(rules=[
 Sequence(rule=Or(rules=[
  family_name,
  generic_family]), regexp='\\s*,\\s*', join_string=',', min_split=1),
 inherit])
font_style = List(values=[
 'normal', 'italic', 'oblique',
 'inherit'])
font_variant = List(values=[
 'normal', 'small-caps',
 'inherit'])
font_weight = List(values=[
 'normal', 'bold', 'bolder', 'lighter',
 '100', '200', '300', '400', '500', '600', '700', '800', '900',
 'inherit'])
font_stretch = List(values=[
 'normal', 'wider', 'narrower', 'ultra-condensed', 'extra-condensed',
 'condensed', 'semi-condensed', 'semi-expanded', 'expanded',
 'extra-expanded', 'ultra-expanded',
 'inherit'])
absolute_and_relative_size = List(values=[
 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'] + [
 'larger', 'smaller'])
font_size = Or(rules=[
 absolute_and_relative_size, positive_length, positive_percentage, inherit])
font_size_adjust = Or(rules=[
 positive_number, none, inherit])
slash_line_height = RegExp(regexp='/%(w)s(?P<s>normal|%(positive-num)s|%(positive-length)s|%(positive-percentage)s|inherit)' % grammar, expand='/\\g<s>')
font = Or(rules=[
 List(values=[
  'caption', 'icon', 'menu', 'message-box', 'small-caption', 'status-bar',
  'inherit']),
 Complex(rules=[
  font_style,
  font_variant,
  font_weight,
  font_size,
  slash_line_height,
  font_family])])