# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_survey/kotti_survey/fanstatic.py
# Compiled at: 2016-06-17 05:39:38
"""
Created on 2016-06-15
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from __future__ import absolute_import
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
library = Library('kotti_survey', 'static')
css = Resource(library, 'styles.css', minified='styles.min.css')
js = Resource(library, 'scripts.js', minified='scripts.min.js')
css_and_js = Group([css, js])