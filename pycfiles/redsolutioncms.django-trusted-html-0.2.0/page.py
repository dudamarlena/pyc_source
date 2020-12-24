# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\page.py
# Compiled at: 2014-04-29 06:05:21
"""
Paged media
http://www.w3.org/TR/1998/REC-CSS2-19980512/page.html
"""
from trustedhtml.classes import List, Or, No
from trustedhtml.rules.css.consts import inherit, auto
from trustedhtml.rules.css.syndata import positive_integer, identifier
size = No()
marks = No()
page_break_before = List(values=[
 'auto', 'always', 'avoid', 'left', 'right',
 'inherit'])
page_break_inside = List(values=[
 'avoid', 'auto',
 'inherit'])
page = Or(rules=[
 identifier, auto])
orphans = Or(rules=[
 positive_integer, inherit])