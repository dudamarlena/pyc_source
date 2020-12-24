# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgcurvycorners\widgets.py
# Compiled at: 2008-03-12 16:41:54
"""this is a TurboGears widget for using CurvyCorners
easily.
http://www.curvycorners.net
"""
import pkg_resources, pkg_resources
from turbogears.widgets import JSLink, Widget, WidgetDescription, register_static_directory
js_dir = pkg_resources.resource_filename('tgcurvycorners', 'static/javascript')
register_static_directory('curvycorners', js_dir)
curvycorners_js = JSLink('curvycorners', 'rounded_corners_lite.inc.js')

class CurvyCorners(Widget):
    """Provides an easy way to use CurvyCorners in your own
    packages.  Exemple:

    from tgcurvycorners import curvycorners
    return dict(jswidget=curvycorners)

    and in your template:

    <span py:strip="True" py:content="jswidget.display()" />

    to get the javascript included. For a detailed usage please
    look at the documentation of the project:

    http://www.curvycorners.net/usage.php

    for a quick and dirty way to use it, insert the following
    code in your html>head:

    ==========================================================
    <script type="text/JavaScript">
      window.onload = function()
      {
        settings = {
          tl: { radius: 20 },
          tr: { radius: 20 },
          bl: { radius: 20 },
          br: { radius: 20 },
          antiAlias: true,
          autoPad: true
        }

        var divObj = document.getElementById("__THEDIVID__");

        var cornersObj = new curvyCorners(settings, divObj);
        cornersObj.applyCornersToAll();
      }
    </script>
    ==========================================================

    make sure you write a real function this is just a dirty
    demo. And make sure you replace "__THEDIVID__" by some real
    div id you want to apply the round corners to.
    """
    javascript = [
     curvycorners_js]


curvycorners = CurvyCorners()

class CurvyCornersDesc(WidgetDescription):
    for_widget = curvycorners
    template = '\n    <div>\n    <script type="text/JavaScript">\n      function curveit(){\n        settings = {\n          tl: { radius: 20 },\n          tr: { radius: 20 },\n          bl: { radius: 20 },\n          br: { radius: 20 },\n          antiAlias: true,\n          autoPad: true\n        }\n\n        var divObj = document.getElementById("demodiv");\n\n        var cornersObj = new curvyCorners(settings, divObj);\n        cornersObj.applyCornersToAll();\n      }\n    </script>\n    <div id="demodiv" onclick="curveit()" style="border:1px solid #000; min-height: 100px; background-color: #ddddee;">\n      <p>\n        Click on this box to see it get round corners...\n      </p>\n      <p>\n        The effect may not be pretty but it proves that it works.\n      </p>\n      <p>\n        For some really cool demos of CurvyCorners please look\n        <a href="http://www.curvycorners.net/">at their website</a>\n      </p>\n    </div>\n    </div>\n    '
    show_separately = True