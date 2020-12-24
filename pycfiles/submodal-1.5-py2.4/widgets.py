# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/submodal/widgets.py
# Compiled at: 2007-04-12 18:35:29
import pkg_resources
from turbogears import widgets
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
static_dir = pkg_resources.resource_filename('submodal', 'static')
register_static_directory('submodal', static_dir)
submodal_css = CSSLink('submodal', 'css/subModal.css')
submodal_js = [JSLink('submodal', 'javascript/subModal.js', location=widgets.js_location.bodytop)]
__all__ = [
 'SubModal']

class SubModal(Widget):
    """
The subModal works by placing a semi-transparent div over the browser,
blocking access to the content below while still providing
visibility. This maintains state and doesn't make someone feel
disoriented or lost by moving them completely to another page. Their
frame of reference is kept while allowing them to perform a new task
(usually closely associated with the content below).
    """
    __module__ = __name__
    css = [
     submodal_css]
    javascript = submodal_js

    def __init__(self, *args, **kwargs):
        super(SubModal, self).__init__(*args, **kwargs)


class SubModalDesc(WidgetDescription):
    __module__ = __name__
    for_widget = SubModal()
    template = '\n    <div>\n      <script type=\'text/javascript\'>\n      var callback_test_function = function (returnVal) {\n          alert(\'This is a callback!\');\n          alert(returnVal);\n      }\n      </script>\n      <p>SubModal Testing.</p>\n      <p><a href=\'http://www.turbogears.org\' class=\'submodal\'>\n         Click Here for a SubModal Window (just using the class is enough ;-))\n         </a></p>\n      <p><a href=\'/tg_widgets/submodal/html/testing.html\'\n         onclick=\'showPopWin("/tg_widgets/submodal/html/testing.html",\n                             500, 300, callback_test_function);\n                  return false;\'>\n         Click Here for a SubModal Window with a CallBack Function</a></p>\n    </div>\n    '