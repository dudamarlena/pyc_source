# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\TGLightWindow\widgets.py
# Compiled at: 2007-08-07 15:24:46
import pkg_resources
from turbogears.widgets import Widget
from turbogears.widgets import CSSLink, JSLink, register_static_directory
from scriptaculous.widgets import prototype_js, scriptaculous_js
__all__ = ['lightwindow_js', 'lightwindow_css', 'LightWindow', 'lightwindow']
pkg_path = pkg_resources.resource_filename(__name__, 'static')
register_static_directory('TGLightWindow', pkg_path)
lightwindow_js = JSLink('TGLightWindow', 'javascript/lightwindow.js')
lightwindow_css = CSSLink('TGLightWindow', 'css/lightwindow.css')

class LightWindow(Widget):
    css = [
     lightwindow_css]
    javascript = [prototype_js, scriptaculous_js, lightwindow_js]


lightwindow = LightWindow()