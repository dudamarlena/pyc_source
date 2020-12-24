# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xcbl/xcbl_widget.py
# Compiled at: 2007-05-09 15:13:32
import pkg_resources
from turbogears import widgets, mochikit
from turbogears.widgets import WidgetDescription
from cherrypy import request
js_dir = pkg_resources.resource_filename('xcbl', 'static/javascript')
register_static_directory('xcbl', js_dir)
xcbl_js = JSLink('xcbl', 'xcbl.js')

class ExtensibleCheckBoxList(widgets.CheckBoxList):
    """A CheckBoxList with an 'Other:' option that accepts hand-entered list items."""
    __module__ = __name__
    javascript = [
     mochikit, xcbl_js]
    template = '\n    <div xmlns:py="http://purl.org/kid/ns#">\n        <script type="text/javascript">\n            function init_${field_id} (event)\n            {\n                MochiKit.Signal.connect("${field_id}_txtEntry", \'onchange\', otherEntered);\n            }\n            MochiKit.Signal.connect(window, \'onload\', init_${field_id});        \n        </script>\n        \n        <ul\n            class="${field_class}"\n            id="${field_id}"\n            py:attrs="list_attrs"\n        >\n            <li py:for="value, desc, attrs in options">\n                <input type="checkbox"\n                    name="${name}"\n                    id="${field_id}_${value}"\n                    value="${value}"\n                    py:attrs="attrs"\n                />\n                <label for="${field_id}_${value}" py:content="desc" />\n            </li>\n            <li id="${field_id}_other_listitem">\n                <input type="checkbox"\n                    name="${name}"\n                    id="${field_id}_other"\n                    value="other"\n                    style="display:none"\n                />\n                <label for="${field_id}_other"\n                    class="fieldlabel">\n                    Other:\n                </label>\n                <input type="text"\n                    checkBoxListName="${name}"\n                    checkBoxListId="${field_id}"\n                    id="${field_id}_txtEntry"            \n                    name="${field_id}_txtEntry"\n                    insert_before="${field_id}_other_listitem"\n                />\n            </li>\n        </ul>\n    </div>'

    def persistingopts(self):
        try:
            selected = request.params.get(self._name)
        except AttributeError:
            return []

        if type(selected) in (str, unicode):
            return [
             selected]
        return selected or []

    def __init__(self, *args, **kwargs):
        opts = kwargs['options']
        if callable(opts):

            def myOptions():
                result = opts()
                return result + [ x for x in self.persistingopts() if x not in result ]

        else:

            def myOptions():
                return opts + [ x for x in self.persistingopts() if x not in opts ]

        kwargs['options'] = myOptions
        super(widgets.CheckBoxList, self).__init__(*args, **kwargs)


class ExtensibleCheckBoxListDesc(WidgetDescription):
    __module__ = __name__
    full_class_name = 'xcbl.ExtensibleCheckBoxList'

    def __init__(self, *args, **kw):
        super(ExtensibleCheckBoxListDesc, self).__init__(*args, **kw)
        self.for_widget = ExtensibleCheckBoxList(name='extensibleCheckBoxList', options=['foo', 'bar'])