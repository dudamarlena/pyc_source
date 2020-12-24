# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/firebug/widgets.py
# Compiled at: 2006-12-20 07:34:41
__all__ = [
 'firebug_css', 'firebug_js', 'firebugx_js']
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
static_dir = pkg_resources.resource_filename('firebug', 'static')
register_static_directory('firebug', static_dir)
firebug_css = CSSLink('firebug', 'css/firebug.css')
firebug_js = JSLink('firebug', 'javascript/firebug.js')
firebugx_js = JSLink('firebug', 'javascript/firebugx.js')