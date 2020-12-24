# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/extjs/grid.py
# Compiled at: 2008-09-03 16:29:00
from tw.api import Widget, JSLink, CSSLink, JSSource
from tw.core.util import Enum, OrderedSet
from tw.extjs import all

class GridJS(JSSource):
    _resources = []
    source_vars = params = [
     'divID', 'width', 'height', 'collapsible', 'title', 'frame']
    src = "Ext.onReady(function() {\n        var myData = {\n  'results': 2, 'rows': [\n    { 'id': 1, 'company': 'Apple', price: 1 },\n    { 'id': 2, 'company': 'Ext', price: 2 } ]\n}\n\n var record = Ext.data.Record.create([\n    {name: 'company'},\n    {name: 'price'}\n]);\n\n         var myReader = new Ext.data.JsonReader({root:'rows', 'id':id}, record);\n\n\tvar grid = new Ext.grid.GridPanel({\n\t\tstore: new Ext.data.Store({\n\t\t\tdata: myData,\n\t\t\treader: myReader\n\t\t}),\n\t\tcolumns: [\n\t\t\t{header: 'Company', resizable:true, sortable: true, dataIndex: 'company'},\n\t\t\t{header: 'Price', sortable: true, dataIndex: 'price'},\n\t\t],\n\t\trenderTo: '${divID}',\n\t\ttitle: 'My First Grid',\n\t\twidth: 500,\n\t\tframe: true,\n                collapsible: true\n\t});\n \n\tgrid.getSelectionModel().selectFirstRow();\n});\n"
    template_engine = 'genshi'
    javascript = [all]

    def update_params(self, d):
        for param in self.source_vars:
            value = getattr(self, param)
            if isinstance(value, bool):
                d[param] = str(value).lower()

        super(GridJS, self).update_params(d)

    def post_init(self, *args, **kw):
        pass

    valid_locations = Enum('head', 'bodytop', 'bodybottom')
    location = valid_locations.bodybottom


class Grid(Widget):
    treeview_js_obj = GridJS
    params = js_params = ['divID']
    template = '<div id="$divID" />'

    def __new__(cls, *args, **kw):
        cls = Widget.__new__(cls, *args, **kw)
        d = {}
        for param in cls.js_params:
            value = getattr(cls, param)
            if value is not None:
                d[param] = getattr(cls, param)

        treeview_js = cls.treeview_js_obj(**d)
        cls.javascript = [treeview_js]
        return cls