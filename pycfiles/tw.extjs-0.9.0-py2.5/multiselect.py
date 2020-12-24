# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/extjs/multiselect.py
# Compiled at: 2008-09-03 16:29:00
from tw.api import Widget, JSLink, CSSLink, JSSource
from tw.core.resources import Resource
from tw.extjs import all
from tw.extjs import all_css, gray_theme
ddview_js = JSLink(modname='tw.extjs', filename='static/DDView.js')
multiselect_css = CSSLink(modname='tw.extjs', filename='static/resources/css/Multiselect.css')
multiselect_js = JSLink(modname='tw.extjs', filename='static/Multiselect.js', javascript=[
 ddview_js], css=[
 multiselect_css])

class ItemSelectorJS(JSSource):
    resources = []
    source_vars = [
     'divID', 'width', 'url', 'fieldLabel', 'labelWidth',
     'fromData', 'toData', 'msWidth', 'msHeight',
     'dataFields', 'valueField', 'displayField',
     'fromLegend', 'toLegend', 'submitText', 'resetText']
    src = '\nformItemSelector = null;\n\npanelItem = {\n            xtype:"itemselector",\n            name:"itemselector",\n            fieldLabel:"$fieldLabel",\n            dataFields:$dataFields,\n            fromData:$fromData,\n            toData:$toData,\n            msWidth:$msWidth,\n            msHeight:$msHeight,\n            valueField:"$valueField",\n            displayField:"$displayField",\n            toLegend:"$toLegend",\n            fromLegend:"$fromLegend",\n            TBar:[{\n                text:"Clear",\n                handler:function(){\n                    var i=formItemSelector.getForm().findField("itemselector");\n                    i.reset.call(i);\n                }\n            }]\n    }\n\nbuttonSave = {\n            text: "$submitText",\n            handler: function() {\n                formItemSelector.getForm().submit(\n                {\n                    method: \'POST\',\n                    waitMsg:\'Submitting...\',\n                    reset : false,\n                    success : function() {\n                        Ext.Msg.alert("Success!");\n                    },\n                    failure: function(form, action){Ext.Msg.alert(\'Error\',action.result.text);}\n                });\n            }\n    }\n\nbuttonReset = {     \n            text:"$resetText",\n            handler: function() {\n                var i=formItemSelector.getForm().findField("itemselector");\n                i.reset.call(i);\n            }\n    }\n\nExt.onReady(function(){\n\n    formItemSelector = new Ext.form.FormPanel({ \n        labelWidth:$labelWidth,\n        width:$width,\n        url:"$url",\n        items:panelItem,\n        buttons:[buttonSave, buttonReset]\n    });\n\n    formItemSelector.render("$divID");\n});\n    '
    template_engine = 'genshi'
    javascript = [all]

    def update_params(self, d):
        for param in self.source_vars:
            value = getattr(self, param)

        super(ItemSelectorJS, self).update_params(d)

    def post_init(self, *args, **kw):
        pass

    location = Resource.valid_locations.head


class ItemSelector(Widget):
    item_selector_js_obj = ItemSelectorJS
    params = js_params = ['divID', 'width', 'url', 'fieldLabel', 'labelWidth',
     'fromData', 'toData', 'msWidth', 'msHeight',
     'dataFields', 'valueField', 'displayField',
     'fromLegend', 'toLegend', 'submitText', 'resetText']
    submitText = 'Submit'
    resetText = 'Reset'
    css = [all_css, multiselect_css]
    template = '\n    <div style="width:600px;">\n        <div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>\n        <div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc">\n          <div id="$divID"></div>\n        </div></div></div>\n        <div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>\n    </div>\n    '

    def __init__(self, *args, **kw):
        super(ItemSelector, self).__init__(*args, **kw)
        d = {}
        for param in self.js_params:
            value = getattr(self, param)
            if value is not None:
                d[param] = getattr(self, param)

        item_selector_js = self.item_selector_js_obj(**d)
        self.javascript = [item_selector_js, multiselect_js]
        return

    def update_params(self, d):
        super(ItemSelector, self).update_params(d)
        if not getattr(d, 'divID', None):
            raise ValueError, 'ItemSelector requires a divID!'
        return