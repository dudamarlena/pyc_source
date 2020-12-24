# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/jquery/widgets.py
# Compiled at: 2008-02-08 10:22:36
"""
jquery and jqwebext
"""
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, register_static_directory, WidgetDescription
js_dir = pkg_resources.resource_filename('jquery', 'static')
register_static_directory('jquery', js_dir)
jquery_js = JSLink('jquery', 'jquery-1.2.3.pack.js')
jquery = jquery_js