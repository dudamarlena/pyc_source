# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\visudet.py
# Compiled at: 2014-04-29 06:05:21
"""
Visual formatting model details
http://www.w3.org/TR/1998/REC-CSS2-19980512/visudet.html
"""
from trustedhtml.classes import List, Or
from trustedhtml.rules.css.consts import inherit, normal, auto, none
from trustedhtml.rules.css.syndata import length, percentage, positive_number, positive_length, positive_percentage
width = Or(rules=[
 positive_length, positive_percentage, auto, inherit])
min_width = Or(rules=[
 positive_length, positive_percentage, inherit])
max_width = Or(rules=[
 positive_length, positive_percentage, none, inherit])
line_height = Or(rules=[
 normal, positive_number, positive_length, positive_percentage, inherit])
vertical_align = Or(rules=[
 List(values=[
  'baseline', 'sub', 'super', 'top', 'text-top', 'middle', 'bottom',
  'text-bottom']),
 length, percentage, inherit])