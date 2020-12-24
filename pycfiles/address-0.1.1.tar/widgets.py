# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/addremoveoptions/widgets.py
# Compiled at: 2009-08-17 14:30:28
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
from turbogears.widgets import *
static_dir = pkg_resources.resource_filename('addremoveoptions', 'static')
register_static_directory('addremoveoptions', static_dir)
add_remove_options_js = JSLink('addremoveoptions', 'javascript/addremoveoptions.js')

class Addremoveoptions(FormField):
    """Creates a selectbox in which you can add options and remove options"""
    template = '\n    <form xmlns:py="http://purl.org/kid/ns#">\n    <select id="selectX" size="8" multiple="multiple">\n    <option value="original1" selected="selected">Original 1</option>\n    <option value="original2">Original 2</option>\n    </select>\n    <br />\n    <input type="button" value="Insert Before Selected" onclick="insertOptionBefore(count1++);" /><br />\n    <input type="button" value="Remove Selected" onclick="removeOptionSelected();" /><br />\n    <input type="button" value="Append Last Entry" onclick="appendOptionLast(count2++);" /><br />\n    <input type="button" value="Remove Last Entry" onclick="removeOptionLast();" />\n    </form>\n \n    '

    def __init__(self, *args, **kw):
        self.javascript = [add_remove_options_js]
        super(Addremoveoptions, self).__init__(*args, **kw)


class Add_remove_optionsDesc(WidgetDescription):
    name = 'Add Remove Options'
    for_widget = Addremoveoptions()
    full_class_name = 'addremoveoptions.Addremoveoptions'