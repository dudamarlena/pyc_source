# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/displayshelf/widgets.py
# Compiled at: 2007-01-18 15:37:37
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
asset_dir = pkg_resources.resource_filename('displayshelf', 'static')
register_static_directory('displayshelf', asset_dir)
displayshelf_js = JSLink('displayshelf', 'javascript/displayshelf.js')
fabridge = JSLink('displayshelf', 'javascript/FABridge.js')

class DisplayShelf(Widget):
    __module__ = __name__
    javascript = [fabridge, displayshelf_js]
    template = "<div><script>insertDisplayShelf('${width}','${height}');showPhotos(${repr(value)});</script></div>"
    params = ['width', 'height']
    params_doc = {'width': 'Width of the Display Shelf', 'height': 'Height of the Display Shelf'}
    width = '100%'
    height = '300'


class DisplayShelfDesc(WidgetDescription):
    __module__ = __name__
    name = 'Display Shelf'
    for_widget = DisplayShelf(default=['/tg_widgets/displayshelf/images/tg_under_the_hood.png', '/tg_widgets/displayshelf/images/under_the_hood_blue.png'])