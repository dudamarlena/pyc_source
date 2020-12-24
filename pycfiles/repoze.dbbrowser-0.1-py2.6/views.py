# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/dbbrowser/views.py
# Compiled at: 2010-03-03 04:44:41
from repoze.bfg.settings import get_settings
from repoze.bfg.url import static_url
from sqlalchemy import Table
from sqlalchemy import types
from sqlalchemy import desc
from repoze.dbbrowser.dbbrowser import DBSession
from repoze.dbbrowser.dbbrowser import Base
DEFAULT_THEME = 'cupertino'
DEFAULT_THEME_SWITCHER = 'false'

def dbbrowser_view(request):
    session = DBSession()
    settings = get_settings()
    app_url = request.application_url
    tables = [ {'name': table.name, 'javascript': table_javascript(app_url, table)} for table in Base.metadata.sorted_tables
             ]
    stat_url = static_url('static', request)
    theme_switcher = False
    theme_switcher_setting = settings.get('theme_switcher', DEFAULT_THEME_SWITCHER)
    if theme_switcher_setting != DEFAULT_THEME_SWITCHER:
        theme_switcher = True
    theme = settings.get('default_theme', DEFAULT_THEME)
    return {'static_url': stat_url, 'tables': tables, 
       'theme': theme, 
       'theme_switcher': theme_switcher}


def table_javascript(url, table):
    table_name = table.name
    viewurl = '%s/tabledata?table=%s' % (url, table_name)
    editurl = '%s/tableedit?table=%s' % (url, table_name)
    table_columns = ("','").join([ column.name for column in table.columns ])
    model_rows = []
    for column in table.columns:
        edittype = 'text'
        if isinstance(column.type, (types.Text, types.TEXT)):
            edittype = 'textarea'
        editrules = '{}'
        if isinstance(column.type, (types.Numeric, types.Integer)):
            editrules = '{number:true}'
        editable = 'true'
        if column.primary_key:
            editable = 'false'
        model_row = "{name:'%(name)s',\n                        index:'%(name)s',\n                        editable:%(editable)s,\n                        editrules:%(editrules)s,\n                        edittype:'%(edittype)s'\n                       }" % {'name': column.name, 'editrules': editrules, 
           'editable': editable, 
           'edittype': edittype}
        model_rows.append(model_row)

    width = 640
    if len(table.columns) > 8:
        width = 860
    if len(table.columns) > 12:
        width = 1024
    table_info = {'url': viewurl, 'editurl': editurl, 'name': table_name, 
       'width': width, 
       'columns': "'%s'" % table_columns, 
       'model': (',\n').join(model_rows)}
    return '\n        jQuery("#table_%(name)s").jqGrid({\n          url:\'%(url)s\',\n          editurl:\'%(editurl)s\',\n          altRows: true,\n          datatype: "json",\n          colNames:[%(columns)s],\n          colModel:[\n                    %(model)s\n          ],\n          rowNum:10,\n          rowList:[10,20,30,40,50],\n          pager: \'#pager_%(name)s\',\n          sortname: \'id\',\n          viewrecords: true,\n          sortorder: "asc",\n          height: "220px",\n          width: %(width)d,\n          caption:"%(name)s"\n        });\n        jQuery("#table_%(name)s").jqGrid(\'navGrid\',\n                                         \'#pager_%(name)s\',\n                                         {}, //options\n                                         {height:380,\n                                          width:450,\n                                          reloadAfterSubmit:false,\n                                          closeAfterEdit:true,\n                                          recreateForm:true}, // edit options\n                                         {height:380,\n                                          width:450,\n                                          reloadAfterSubmit:true,\n                                          closeAfterAdd:true,\n                                          recreateForm:true}, // add options\n                                         {reloadAfterSubmit:false}, // del options\n                                         {} // search option\n                                        );\n    ' % table_info


def tabledata_view(request):
    table_name = request.GET['table']
    session = DBSession()
    page = request.GET.get('page', '1')
    limit = request.GET.get('rows', '10')
    sidx = request.GET.get('sidx', 'id')
    sord = request.GET.get('sord', '')
    search = request.GET.get('_search', 'false')
    page = int(page)
    limit = int(limit)
    offset = (page - 1) * limit
    table = Table(table_name, Base.metadata)
    table_columns = [ column.name for column in table.columns ]
    query = session.query(table)
    if sidx in table_columns and sord == 'asc':
        query = query.order_by(sidx)
    if sidx in table_columns and sord == 'desc':
        query = query.order_by(desc(sidx))
    if search == 'true':
        searchField = request.GET.get('searchField', None)
        searchOper = request.GET.get('searchOper', None)
        searchString = request.GET.get('searchString', None)
        filter = get_filter(searchField, searchOper, searchString)
        query = query.filter(filter)
    count = query.count()
    query = query.offset(offset)
    rows = [ {'id': row[0], 'cell': row} for row in query.limit(limit)
           ]
    pages = int((count - 1) / limit) + 1
    data = {'rows': rows, 'page': page, 
       'total': pages, 
       'records': count}
    return data


def tableedit_view(request):
    session = DBSession()
    table_name = request.GET['table']
    table = Table(table_name, Base.metadata)
    bind = table.bind
    table_columns = [ column.name for column in table.columns ]
    oper = request.POST.get('oper', None)
    if oper == 'del':
        id = request.POST['id']
        session.query(table).filter('id=%s' % id).delete(synchronize_session=False)
        session.commit()
        session.flush()
    if oper == 'add':
        values = {}
        for (key, value) in request.POST.items():
            if key in table_columns and key != 'id':
                values[key] = unicode(value)

        insert = table.insert(values)
        session.execute(insert)
        session.commit()
        session.flush()
    if oper == 'edit':
        values = {}
        for (key, value) in request.POST.items():
            if key in table_columns and key != 'id':
                values[key] = unicode(value)

        id = request.POST['id']
        session.query(table).filter('id=%s' % id).update(values, synchronize_session=False)
        session.commit()
        session.flush()
    return 'ok'


def get_filter(field, op, string):
    if op == 'eq':
        return "%s='%s'" % (field, string)
    if op == 'ne':
        return "%s<>'%s'" % (field, string)
    if op == 'lt':
        return "%s<'%s'" % (field, string)
    if op == 'gt':
        return "%s>'%s'" % (field, string)
    if op == 'le':
        return "%s<='%s'" % (field, string)
    if op == 'ge':
        return "%s>='%s'" % (field, string)
    if op == 'bw':
        return "%s like '%s%%'" % (field, string)
    if op == 'bn':
        return "%s not like '%s%%'" % (field, string)
    if op == 'ew':
        return "%s like '%%%s'" % (field, string)
    if op == 'en':
        return "%s not like '%%%s'" % (field, string)
    if op == 'in':
        splitchar = ' '
        if '|' in string:
            splitchar = '|'
        wordlist = ("','").join(string.split(splitchar))
        return "%s in ('%s')" % (field, wordlist)
    if op == 'ni':
        splitchar = ' '
        if '|' in string:
            splitchar = '|'
        wordlist = ("','").join(string.split(splitchar))
        return "%s not in ('%s')" % (field, wordlist)
    if op == 'cn':
        return "%s like '%%%s%%'" % (field, string)
    if op == 'nc':
        return "%s not like '%%%s%%'" % (field, string)