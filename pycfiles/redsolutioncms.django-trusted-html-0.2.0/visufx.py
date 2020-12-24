# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\css\visufx.py
# Compiled at: 2014-04-29 06:05:21
"""
Visual effects
http://www.w3.org/TR/1998/REC-CSS2-19980512/visufx.html
"""
from trustedhtml.classes import List, RegExp, Or
from trustedhtml.rules.css.consts import auto, inherit
from trustedhtml.rules.css.grammar import grammar
overflow = List(values=[
 'visible', 'hidden', 'scroll', 'auto',
 'inherit'])
clip_shape = RegExp(regexp='(?P<n>rect)\\(%(w)s(?P<a>%(length)s|auto)%(w)s\\,%(w)s(?P<b>%(length)s|auto)%(w)s\\,%(w)s(?P<c>%(length)s|auto)%(w)s\\,%(w)s(?P<d>%(length)s|auto)%(w)s\\)$' % grammar, expand='\\g<n>(\\g<a>,\\g<b>,\\g<c>,\\g<d>)')
clip = Or(rules=[
 clip_shape, auto, inherit])
visibility = List(values=[
 'visible', 'hidden', 'collapse',
 'inherit'])