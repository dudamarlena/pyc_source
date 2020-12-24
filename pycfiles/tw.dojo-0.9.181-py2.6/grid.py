# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tw/dojo/grid.py
# Compiled at: 2013-01-02 11:28:41
from tw.dojo.core import DojoBase, JSONHash, DojoCSSLink
from tw.api import JSLink, JSSource, CSSLink, CSSSource, Widget, js_function, locations
from tw.core.resources import JSDynamicFunctionCalls
grid_css = DojoCSSLink(basename='dojox/grid/resources/Grid')
tundra_grid_css = DojoCSSLink(basename='static/dojox/grid/resources/tundraGrid')
dojoquerygrid = JSLink(filename='/static/twdojo/grid.js', css=[
 grid_css])
buildGrid = JSSource(src='\n    function buildGrid(grid_node,grid_params){\n        for (var i in grid_params.attributes.structure) {\n            for (var j in grid_params.attributes.structure[i]) {\n                if (grid_params.attributes.structure[i][j].type) grid_params.attributes.structure[i][j].type=eval(grid_params.attributes.structure[i][j].type);\n                if (grid_params.attributes.structure[i][j].widgetClass) grid_params.attributes.structure[i][j].widgetClass=eval(grid_params.attributes.structure[i][j].widgetClass);\n                if (grid_params.attributes.structure[i][j].formatter) grid_params.attributes.structure[i][j].formatter=eval(grid_params.attributes.structure[i][j].formatter);\n            }\n        }\n        if (grid_params.attributes.store) grid_params.attributes.store=eval(grid_params.attributes.store);\n        //if (grid_params.attributes.store) grid_params.store=dojo.byId(grid_params.attributes.store);\n        grid_params.id="grid_"+grid_node\n        grid = new dojox.grid.DataGrid(grid_params.attributes, grid_node);\n\t\tgrid.startup();\n\t\t};\n    ')

class GridColumn(JSONHash):
    skip_attributes = True
    properties = ['field', 'name', 'width', 'rowSpan', 'hidden', 'colSpan', 'styles', 'type', 'editable', 'widgetClass', 'formatter', 'options', 'constraint', 'editorToolbar']


class GridParams(JSONHash):
    attributes_list = [
     'structure', 'sortInfo', 'columnReordering', 'selectionMode', 'rowCount', 'elasticView', 'rowsPerPage', 'columnToggling', 'autoWidth', 'keepRows']
    columns = {}

    def addColumn(self, *column, **kwargs):
        row = kwargs.get('row', -1)
        if column and isinstance(column[0], GridColumn):
            column = column[0]
        else:
            column = GridColumn(**kwargs)
        if self['attributes'].get('structure'):
            self['attributes']['structure'][row].append(column)
        else:
            self['attributes']['structure'] = [
             [
              column]]
        self.columns[column['name'].lower()] = len(self.columns) + 1

    def addColumns(self, columns):
        self['attributes']['structure'] = columns

    def addRow(self, *series, **kwargs):
        if self['attributes'].get('structure'):
            self['attributes']['structure'].append([])
        else:
            self['attributes']['structure'] = [[]]

    def setAttr(self, attr, value):
        self['attributes'][attr] = value

    def setSort(self, column, ascending=True):
        if isinstance(column, GridColumn):
            sort_col = self.columns.get(column['name'].lower(), None)
        elif isinstance(column, str):
            sort_col = self.columns.get(column.lower(), None)
        elif isinstance(column, int):
            sort_col = column
        if sort_col:
            if not ascending:
                sort_col = sort_col * -1
            self['attributes']['sortInfo'] = sort_col
        return


class DojoGrid(DojoBase):
    """
    Dojo grid widget, to build the structure just pass the columns attribute as a DojoGridColumn list
    and a Dojo store where data is stored
    pylons.c.grid = DojoGrid()
    pylons.c.grid.addColumn(field='customer_id',name='id')
    pylons.c.grid.addColumn(field='name',name='Name')
    pylons.c.grid.addColumn(field='phone',name='Phone Number',width='auto')

    ${grid(id='grid',query="{customer_id:'*'}",store='sample_store')}
    use attrs to specify extra attrs
    """
    css = [
     grid_css, tundra_grid_css]
    javascript = [buildGrid]
    require = ['dojox.grid.DataGrid']
    dojoType = 'dojox.grid.DataGrid'
    params = ['style', 'cssclass', 'query', 'attrs', 'clientSort', 'store', 'rowsPerPage', 'sortFields', 'grid_search_attrs']
    attrs = {}
    grid_search_attrs = {}
    style = None
    cssclass = None
    name = None
    query = None
    store = ''
    clientSort = 'true'
    rowsPerPage = 30
    columns = []
    include_dynamic_js_calls = True
    attrs = {'escapeHTMLinData': False}
    template = '\n    <span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip="">\n    <div id=\'grid_container_${id}\' py:attrs="{\'style\':style,\'class\':cssclass}" >\n    <div id=\'${id}\' py:attrs="dict(attrs)" />\n    </div>\n    <script type=\'text/javascript\'>\n        dojo.addOnLoad(function(){buildGrid(\'${id}\',${grid_params});});\n    </script>\n    </span>\n    '

    def __init__(self, **kw):
        self.gparams = kw.get('grid_params', GridParams(**kw))

    def update_params(self, d):
        super(DojoGrid, self).update_params(d)
        for attr in ['store', 'query', 'rowsPerPage']:
            if d.get(attr):
                self.gparams.setAttr(attr, d.get(attr))

        d['grid_params'] = self.gparams.json()

    def addColumn(self, *args, **kwargs):
        self.gparams.addColumn(*args, **kwargs)

    def addColumns(self, *args, **kwargs):
        self.gparams.addColumns(*args, **kwargs)

    def addRow(self, *args, **kwargs):
        self.gparams.addRow(*args, **kwargs)

    def setSort(self, *args, **kwargs):
        self.gparams.setSort(*args, **kwargs)


class DojoGridSearchBox(DojoBase):
    require = [
     'dijit.form.TextBox', 'dijit.form.DateTextBox', 'dijit.form.FilteringSelect', 'dijit.form.Button']
    javascript = [dojoquerygrid]
    params = ['grid']
    grid = ''
    template = '<div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip=""><div id="querybox_${grid}">\n        <div id="queryrow_${grid}_1">\n        <select id="field_${grid}_1" dojoType="dijit.form.FilteringSelect" autocomplete="false" onChange="changeWidget(this)">\n        <option selected="selected" value=\'id\'>Id</option>\n        <option value=\'ragione_sociale\'>Ragione Sociale</option>\n        <option value=\'codice_fiscale\'>Codice Fiscale</option>\n        </select>\n        <span id=\'opbox_${grid}_1\'>\n        <select type=\'text\' id=\'operator_${grid}_1\' dojoType=\'dijit.form.FilteringSelect\' autocomplete=\'false\' onChange=\'changeWidget(this)\'>\n            <option selected=\'selected\' value=\'equal\'>=</option>\n            <option value=\'not_equal\'>!=</option>\n            </select>\n        </span>\n        <span id=\'valuebox_grid_1\'>\n        <input type=\'text\' dojoType=\'dijit.form.TextBox\' id=\'value_${grid}_1\' /></span>\n        </div></div>\n        <button dojoType=\'dijit.form.Button\' id=\'search_${grid}\' onClick="doSearch(\'${grid}\')">\n        Search\n        </button>\n        <button dojoType=\'dijit.form.Button\' id=\'add_${grid}\' onClick="addElement(\'${grid}\')">\n        Add line\n        </button></div>\n    '