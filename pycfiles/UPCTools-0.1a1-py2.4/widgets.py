# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\upc_tools\widgets.py
# Compiled at: 2006-12-11 10:18:00
import pkg_resources
from turbogears.widgets import register_static_directory, TextField, JSLink, RPC, Button
from turbogears.validators import FancyValidator
from div_dialogs.widgets import DialogBoxLink
static = pkg_resources.resource_filename('upc_tools', 'static')
register_static_directory('upc_tools_static', static)
static = 'upc_tools_static'

class UPCValidator(FancyValidator):
    __module__ = __name__

    def _to_python(self, value, state):
        return value

    def _from_python(self, value, state):
        return value


class UPCLookupField(TextField):
    __module__ = __name__
    template = '\n    <div xmlns:py="http://purl.org/kid/ns#">\n        <input type="text" name="${name}" class="${field_class}"\n               id="${field_id}" value="${value}" py:attrs="attrs" />\n        <span style="font-size: small">\n            ${dialog.display(dom_id=\'%s_dialog\' % field_id, on_open=\'getElement("%s_upc_search").value = getElement("%s").value; getElement("%s_upc_search_button").onclick();\' % (field_id, field_id, field_id))}\n        </span>\n        <div id="${field_id}_dialog" style="position: absolute; visibility: hidden;">\n            <div style="padding: 3px">\n                <div>\n                    <script type="text/javascript">\n                        function search_upc_if_enter(e) {\n                            if (window.event) {\n                                e = window.event;\n                            }\n                            if (e.keyCode == 13) {\n                                button = getElement(\'${field_id}_upc_search_button\');\n                                button.onclick();\n                                return false;\n                            }\n                            return true;\n                        }\n                    </script>\n                    UPC <input type="text" id="${field_id}_upc_search" name="tg_random" onkeypress="return search_upc_if_enter(event)" />\n                    <input id="${field_id}_upc_search_button" type="button" value="Check" onclick="return ajax_upc_lookup(\'${field_id}_upc_search\', \'${field_id}_upc_lookup_results\');" />\n                </div>\n                <div id="${field_id}_upc_lookup_results" style="margin-top: 5px">\n                </div>\n            </div>\n        </div>\n    </div>\n    '
    params = [
     'form', 'dialog']
    javascript = [JSLink(static, 'upc_tools.js')]

    def __init__(self, *args, **kw):
        super(UPCLookupField, self).__init__(*args, **kw)
        self.javascript.extend(RPC.javascript)
        self.dialog = DialogBoxLink(link_text='Check Online', title='Online UPC Lookup', height=255)
        self.javascript.extend(self.dialog.javascript)
        self.css.extend(self.dialog.css)
        self.validator = UPCValidator()