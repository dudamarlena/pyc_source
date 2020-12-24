# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/yuiwidget/table.py
# Compiled at: 2008-11-03 17:12:49
"""
$Id: $
"""
from zc.table import table
from zc.resourcelibrary import need
from zope.traversing.browser import absoluteURL
table_js_template = '\n<script type="text/javascript">\n    YAHOO.util.Event.onDOMReady(function(){\n  \n    var datasource, columns, config\n\n    // Setup Datasource for Container Viewlet\n    datasource = new YAHOO.util.DataSource("%(data_url)s");\n    datasource.responseType   = YAHOO.util.DataSource.TYPE_JSON;\n    datasource.responseSchema = {\n      resultsList: "nodes",\n      fields: [ %(fields)s ],\n      metaFields: { totalRecords: "length", sortKey:"sort", sortDir:"dir", paginationRecordOffset:"start"}\n      }\n      \n    columns = [ %(columns)s ];\n    \n    // A custom function to translate the js paging request into a datasource query \n    var buildQueryString = function (state,dt) {\n        sDir = (dt.get("sortedBy").dir === "asc"||dt.get("sortedBy").dir == "") ? "" : "desc";\n        var query_url = "start=" + state.pagination.recordOffset + "&limit=" + state.pagination.rowsPerPage + "&sort=" + dt.get("sortedBy").key  + "&dir="+sDir;\n        return query_url\n    };\n    \n    config = {\n       paginator : %(paginator)s,\n       initialRequest : \'start=0&limit=20\',\n       generateRequest : buildQueryString,\n       paginationEventHandler : YAHOO.widget.DataTable.handleDataSourcePagination,\n       %(js_default_sort)s,\n       %(js_config)s\n    }\n\n    table = new YAHOO.widget.DataTable( YAHOO.util.Dom.get("%(table_id)s"), columns, datasource, config  )    \n    table.sortColumn = function(oColumn) {\n        // Default ascending\n        var sDir = "asc";\n        \n        // If already sorted, sort in opposite direction\n        if(oColumn.key === this.get("sortedBy").key) {\n           sDir = (this.get("sortedBy").dir === "asc"||this.get("sortedBy").dir == "") ? "desc" : "asc";\n           }\n\n        // Pass in sort values to server request\n        var newRequest = "sort=" + oColumn.key + "&dir=" + sDir + "&start=0";\n        // Create callback for data request\n        var oCallback = {\n                success: this.onDataReturnInitializeTable,\n                failure: this.onDataReturnInitializeTable,\n                scope: this,\n                argument: {\n                    // Pass in sort values so UI can be updated in callback function\n                    sorting: {\n                        key: oColumn.key,\n                        dir: (sDir === "asc") ? YAHOO.widget.DataTable.CLASS_ASC : YAHOO.widget.DataTable.CLASS_DESC\n                    }\n                }\n            }\n            \n        // Send the request\n        this.getDataSource().sendRequest(newRequest, oCallback);\n        \n        };\n        \n    table.subscribe("rowMouseoverEvent", table.onEventHighlightRow); \n    table.subscribe("rowMouseoutEvent", table.onEventUnhighlightRow);\n    %(js_extra)s\n});\n</script>\n'

class BaseDataTableFormatter(table.Formatter):
    data_view = '/@@json'
    prefix = ''
    paginator = 'new YAHOO.widget.Paginator({ rowsPerPage : 20 })'
    js_extra = ''
    js_config = ''
    js_default_sort = ''

    def __init__(self, context, request, items, paginator=None, data_view=None, *args, **kw):
        super(BaseDataTableFormatter, self).__init__(context, request, items, *args, **kw)
        if paginator:
            self.paginator = paginator
        if data_view:
            self.data_view = data_view

    def renderExtra(self):
        need('yui-datatable')
        extra = table_js_template % self.getDataTableConfig()
        return extra

    def getFields(self):
        """ return zope.schema fields that should be displayed """
        raise NotImplemented

    def getDataTableConfig(self):
        """
        fields
        columns
        table_id
        """
        config = {}
        (config['columns'], config['fields']) = self.getFieldColumns()
        config['data_url'] = self.getDataSourceURL()
        config['table_id'] = self.prefix
        config['paginator'] = self.paginator
        config['js_extra'] = self.js_extra
        config['js_config'] = self.js_config
        config['js_default_sort'] = self.js_default_sort or 'sortedBy : { key: "na", dir : "asc" }'
        return config

    def __call__(self):
        return '<div id="%s">\n<table %s>\n%s</table>\n%s</div>' % (
         self.prefix,
         self._getCSSClass('table'), self.renderContents(),
         self.renderExtra())

    def getFieldColumns(self):
        column_model = []
        field_model = []
        for field in self.getFields():
            key = field.__name__
            column_model.append('{key:"%s", label:"%s", sortable:true}' % (key, field.title))
            field_model.append('{key:"%s"}' % key)

        return (
         (',').join(column_model), (',').join(field_model))

    def getDataSourceURL(self):
        url = absoluteURL(self.context, self.request)
        url += self.data_view + '?'
        return url


class ContainerDataTableFormatter(BaseDataTableFormatter):
    data_view = '/@@json'
    prefix = 'datacontents_id'

    def getFields(self):
        import alchemist.ui.container
        return alchemist.ui.container.getFields(self.context)


class ContextDataTableFormatter(BaseDataTableFormatter):
    pass