# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\div_dialogs\widgets.py
# Compiled at: 2007-02-28 07:59:19
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
from scriptaculous import prototype_js, scriptaculous_js
from turbojson import jsonify
js_dir = pkg_resources.resource_filename('div_dialogs', 'static/javascript')
register_static_directory('div_dialogs.js', js_dir)
css_dir = pkg_resources.resource_filename('div_dialogs', 'static/css')
register_static_directory('div_dialogs.css', css_dir)
js_dir = 'div_dialogs.js'
css_dir = 'div_dialogs.css'
themes_dir = css_dir + '/themes'
dimming_div_js = JSLink(js_dir, 'dimmingdiv.js')
dimming_div_css = CSSLink(css_dir, 'dimming.css')

class DialogBox(Widget):
    __module__ = __name__
    javascript = [dimming_div_js, scriptaculous_js]
    css = [
     dimming_div_css]
    template = '\n    <script xmlns:py="http://purl.org/kid/ns#" type="text/javascript">\n        function show_${dom_id}_window() {\n            open_dialog(\'${dom_id}\', \'${title}\', \'${width}\', \'${height}\', ${x}, ${y}, ${modal and \'true\' or \'false\'}, \'${on_open}\', \'${on_close}\');\n        }\n        ${dom_id}_window = {show: show_${dom_id}_window};\n        <div py:if="show" py:strip="True">\n        ${dom_id}_window.show();\n        </div>\n    </script>\n    '
    params = [
     'dom_id', 'title', 'width', 'height', 'x', 'y', 'modal', 'show', 'on_open', 'on_close']
    params_doc = {'dom_id': 'ID of the DOM object that will be converted to a dialog box'}
    title = ''
    width = 400
    height = 200
    x = -1
    y = -1
    modal = False
    show = False


class DialogBoxLink(Widget):
    __module__ = __name__
    javascript = [dimming_div_js, scriptaculous_js]
    css = [
     dimming_div_css]
    template = '\n    <span xmlns:py="http://purl.org/kid/ns#">\n        <a href="javascript:open_dialog(\'${dom_id}\', \'${title}\', \'${width}\', \'${height}\', ${x}, ${y}, ${modal and \'true\' or \'false\'}, \'${on_open}\', \'${on_close}\')">\n            ${link_text}\n        </a>\n    </span>\n    '
    params = [
     'dom_id', 'link_text', 'title', 'width', 'height', 'x', 'y', 'modal', 'on_open', 'on_close']
    params_doc = {'dom_id': 'ID of the DOM object that will be converted to a dialog box'}
    title = ''
    width = 400
    height = 200
    x = -1
    y = -1
    modal = False


class DialogBoxLinkDescription(WidgetDescription):
    __module__ = __name__
    for_widget = DialogBoxLink()
    name = 'Dialog Box Link'
    template = '\n        <div xmlns:py="http://purl.org/kid/ns#">\n            Click ${for_widget.display(link_text=\'here\', title=\'Greetings!\', dom_id=\'dialog_box\',)}\n            to open the dialog.<br/>\n            Click ${for_widget.display(link_text=\'here\', title=\'Greetings!\', dom_id=\'dialog_box\', modal=True)}\n            to see the modal version.\n            <div id="dialog_box" style="position: absolute; visibility: hidden;">\n                <h1>Hello there!</h1>\n            </div>\n        </div>\n    '


window_js = JSLink(js_dir, 'window.js')
window_ext_js = JSLink(js_dir, 'window_ext.js')
debug_js = JSLink(js_dir, 'debug.js')
default_css = CSSLink(themes_dir, 'default.css')
alphacube_css = CSSLink(themes_dir, 'alphacube.css')

class BaseWindow(Widget):
    __module__ = __name__
    template = '\n    <script xmlns:py="http://purl.org/kid/ns#" type="text/javascript">\n        window.${id} = new Window(\'${id}\', ${options});\n        function display(e) {\n            ${id}.toFront();\n            ${id}.setContent(\'${dom_id}\',\n                             ${inherit_dimensions and \'true\' or \'false\'},\n                             ${inherit_position and \'true\' or \'false\'});\n            <div py:if="show" py:strip="True">${id}.${show_func}(${modal and \'true\' or \'false\'});</div>\n        }\n        Event.observe(window, \'load\', display);\n    </script>\n    '
    css = [
     CSSLink(themes_dir, 'default.css'), CSSLink(themes_dir, 'alphacube.css')]
    javascript = [
     prototype_js, window_js]
    params = [
     'dom_id', 'link_text', 'title', 'width', 'height', 'x', 'y', 'modal', 'on_open', 'on_close', 'centered', 'resizable', 'show', 'theme', 'minimizable', 'maximizable', 'closable', 'draggable', 'wired_drag']
    width = -1
    height = -1
    x = -1
    y = -1
    static = True
    show = False
    title = ''
    centered = False
    modal = False
    resizable = True
    minimizable = True
    maximizable = True
    draggable = True
    closable = True
    theme = 'alphacube'
    wired_drag = False

    def get_options(self, d):
        opt = dict()
        opt['className'] = d['theme']
        opt['wiredDrag'] = d['wired_drag']
        for i in ['minimizable', 'maximizable', 'closable', 'theme', 'title', 'draggable']:
            opt[i] = d[i]

        if d.get('x') >= 0 or d.get('y') >= 0:
            d['inherit_position'] = False
            opt['left'] = int(d['x'])
            opt['top'] = int(d['y'])
        else:
            d['inherit_position'] = True
        if d.get('width') >= 0 or d.get('height') >= 0:
            d['inherit_dimensions'] = False
            opt['height'] = int(d['height'])
            opt['width'] = int(d['width'])
        else:
            d['inherit_dimensions'] = True
        return opt

    def update_params(self, d):
        super(BaseWindow, self).update_params(d)
        d['options'] = jsonify.encode(self.get_options(d))
        if d['centered']:
            d['show_func'] = 'showCenter'
        else:
            d['show_func'] = 'show'
        d['id'] = d['dom_id'] + '_window'


class AjaxWindow(BaseWindow):
    __module__ = __name__
    template = '\n    <script xmlns:py="http://purl.org/kid/ns#" type="text/javascript">\n        window.${id} = new Window(\'${id}\', ${options});\n        function init(e) {\n            ${id}.toFront();\n            <div py:if="show" py:strip="True">${id}.${show_func}(${modal and \'true\' or \'false\'});</div>\n        }\n        Event.observe(window, \'load\', init);\n    </script>\n    '
    params = [
     'url']

    def get_options(self, d):
        opt = super(AjaxWindow, self).get_options(d)
        opt['url'] = d['url']
        return opt


class Window(BaseWindow):
    __module__ = __name__
    template = '\n    <script xmlns:py="http://purl.org/kid/ns#" type="text/javascript">\n        window.${id} = new Window(\'${id}\', ${options});\n        function init(e) {\n            ${id}.toFront();\n            ${id}.setContent(\'${dom_id}\',\n                             ${inherit_dimensions and \'true\' or \'false\'},\n                             ${inherit_position and \'true\' or \'false\'});\n            <div py:if="show" py:strip="True">${id}.${show_func}(${modal and \'true\' or \'false\'});</div>\n        }\n        Event.observe(window, \'load\', init);\n    </script>\n    '


class WindowDescription(WidgetDescription):
    __module__ = __name__
    for_widget = Window()
    name = 'Window'
    template = '\n    <div xmlns:py="http://purl.org/kid/ns#">\n        <div id="my_window" style="width: 300px">\n            This is a div.<br/>\n            This is a div.<br/>\n            This is a div.<br/>\n            This is a div.<br/>\n            <form>\n                 Test: <input type="text" />\n            </form>\n        </div>\n        ${for_widget.display(dom_id=\'my_window\', show=True)}\n    </div>\n    '
    show_separately = True


class StaticWindow(Widget):
    __module__ = __name__
    template = '\n    <div xmlns:py="http://purl.org/kid/ns#">\n        Static window goes here\n    </div>\n    '


class StaticWindowDescription(Widget):
    __module__ = __name__
    for_widget = StaticWindow()