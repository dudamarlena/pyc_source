# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_contenttypes/kotti_contenttypes/fanstatic.py
# Compiled at: 2017-01-26 14:33:08
"""
Created on 2016-10-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from __future__ import absolute_import
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
library = Library('kotti_contenttypes', 'static')
pagination_js = Resource(library, 'ext/list.pagination.js/dist/list.pagination.min.js')
list_js = Resource(library, 'list.min.js', depends=[pagination_js])
folder_js = Group([
 Resource(library, 'folder.js', depends=[list_js]),
 Resource(library, 'folder.css')])
css = Resource(library, 'styles.css', minified='styles.min.css')
js = Resource(library, 'scripts.js', minified='scripts.min.js')
css_and_js = Group([css, js])