# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/workspace/osoobe/packages/kotti/kotti_theme_sbadmin/kotti_theme_sbadmin/fanstatic.py
# Compiled at: 2016-10-24 02:58:42
"""
Created on 2016-10-24
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from __future__ import absolute_import
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
library = Library('kotti_theme_sbadmin', 'static')
css = Resource(library, 'styles.css')
js = Resource(library, 'scripts.js')
css_and_js = Group([css, js])