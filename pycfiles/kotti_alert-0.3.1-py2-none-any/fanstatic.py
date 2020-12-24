# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/environment/dpisonline/src/kotti_alert/kotti_alert/fanstatic.py
# Compiled at: 2019-09-18 14:40:37
"""
Created on 2016-07-01
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from __future__ import absolute_import
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
library = Library('kotti_alert', 'static')
css = Resource(library, 'styles.css', minified='styles.min.css')
cookie = Resource(library, 'js.cookie.js')
js = Resource(library, 'scripts.js', depends=[
 cookie], minified='scripts.min.js')
css_and_js = Group([css, js])