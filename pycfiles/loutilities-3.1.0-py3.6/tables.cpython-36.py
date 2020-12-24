# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\tables.py
# Compiled at: 2020-02-11 16:46:57
# Size of source mod 2**32: 118524 bytes
from collections import defaultdict
import traceback
from copy import deepcopy, copy
from json import dumps
from urllib.parse import urlencode
from threading import RLock
import sys, flask
from flask import request, jsonify, url_for, current_app, make_response
from flask.views import MethodView
from sqlalchemy import func, types, cast
from sqlalchemy.types import TypeDecorator
from datatables import DataTables as BaseDataTables, ColumnDT
from loutilities.nesteddict import NestedDict

class ParameterError(Exception):
    pass


class NotImplementedError(Exception):
    pass


class staleData(Exception):
    pass


debug = False
SEPARATOR = ', '
REGEX_URL = '^(http:\\/\\/www\\.|https:\\/\\/www\\.|http:\\/\\/|https:\\/\\/)?[a-zA-Z0-9]+([\\-\\.]{1}[a-zA-Z0-9]+)*\\.[a-zA-Z]{2,5}(:[0-9]{1,5})?(\\/.*)?$'
REGEX_EMAIL = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,63}$'
REGEX_VBL = '^[a-zA-Z_$][a-zA-Z_$0-9]*$'

class RenderBoolean(TypeDecorator):
    impl = types.String

    def __init__(self, *args, **kwargs):
        self.truedisplay = kwargs.pop('truedisplay')
        self.falsedisplay = kwargs.pop('falsedisplay')
        (super(RenderBoolean, self).__init__)(*args, **kwargs)

    def process_result_value(self, value, engine):
        if int(value):
            return self.truedisplay
        else:
            return self.falsedisplay


def renderboolean(expr, *args, **kwargs):
    return cast(expr, RenderBoolean(*args, **kwargs))


def get_dbattr(basemodel, attrstring):
    """
    get a database attribute for a string which may have multiple levels

    :param basemodel: top level model under which attrstring should be found
    :param attrstring: dotted notation attribute; dots allow traversal of multiple levels
    :return: bottom level attribute value
    """
    attrs = attrstring.split('.')
    thismodel = basemodel
    while len(attrs) > 1:
        thisattr = attrs.pop(0)
        thismodel = type(getattr(thismodel, thisattr))

    attr = attrs.pop(0)
    return getattr(thismodel, attr)


def dt_editor_response(**respargs):
    """
    build response for datatables editor
    
    :param respargs: arguments for response
    :rtype: json response
    """
    return (flask.jsonify)(**respargs)


def get_request_action(form):
    """
    return dict list with data from request.form

    :param form: MultiDict from `request.form`
    :rtype: action - 'create', 'edit', or 'remove'
    """
    if 'action' in form:
        return form['action']
    else:
        return


def get_request_data(form):
    """
    return dict list with data from request.form

    :param form: MultiDict from `request.form`
    :rtype: {id1: {field1:val1, ...}, ...} [fieldn and valn are strings]
    """
    data = defaultdict(lambda : {})
    for formkey in list(form.keys()):
        if formkey[0:5] != 'data[':
            pass
        else:
            formlineitems = formkey.split('[')
            datapart, idpart = formlineitems[0:2]
            idvalue = int(idpart[0:-1])
            fieldparts = [part[0:-1] for part in formlineitems[2:]]
            fieldkey = '.'.join(fieldparts)
            fieldlevels = NestedDict()
            fieldlevels[fieldkey] = form[formkey]
            data[idvalue].update(fieldlevels.to_dict())
            if debug:
                from pprint import PrettyPrinter
                pp = PrettyPrinter()
                current_app.logger.debug('get_request_data(): formkey={} data={}'.format(formkey, pp.pformat(data)))

    return data


def alt_yadcf_range_number(expr, value):
    v_from, v_to = value.split('-yadcf_delim-')
    v_from = float(v_from) if v_from != '' else -sys.maxsize + 1
    v_to = float(v_to) if v_to != '' else sys.maxsize
    return expr.between(v_from, v_to)


from datatables.search_methods import SEARCH_METHODS
SEARCH_METHODS['yadcf_range_number'] = alt_yadcf_range_number

class DataTables(BaseDataTables, object):

    def __init__(self, *args, **kwargs):
        self.set_yadcf_data = kwargs.pop('set_yadcf_data', None)
        (super(DataTables, self).__init__)(*args, **kwargs)

    def _set_yadcf_data(self, query):
        if self.set_yadcf_data:
            self.yadcf_params = self.set_yadcf_data()
        else:
            super(DataTables, self)._set_yadcf_data(query)


class DataTablesEditor:
    __doc__ = "\n    handle CRUD request from dataTables Editor\n\n    dbmapping is dict like {'dbattr_n':'formfield_n', 'dbattr_m':f(form), ...}\n    formmapping is dict like {'formfield_n':'dbattr_n', 'formfield_m':f(dbrow), ...}\n    if order of operation is importand use OrderedDict\n\n    If dbattr key == '__skip__', then don't try to update the db with this field\n\n    :param dbmapping: mapping dict with key for each db field, value is key in form or function(dbentry)\n    :param formmapping: mapping dict with key for each form row, value is key in db row or function(form)\n    :param null2emptystring: if True translate '' from form to None for db and visa versa\n    "

    def __init__(self, dbmapping, formmapping, null2emptystring=False):
        self.dbmapping = dbmapping
        self.formmapping = formmapping
        self.null2emptystring = null2emptystring

    def get_response_data(self, dbentry, nesteddata=False):
        """
        set form values based on database model object

        :param dbentry: database entry (model object)
        :param nesteddata: set to True if data coming from server is multi leveled e.g., see see https://editor.datatables.net/examples/simple/join.html)
        """
        if nesteddata:
            data = NestedDict()
        else:
            data = {}
        for key in self.formmapping:
            if hasattr(self.formmapping[key], '__call__'):
                callback = self.formmapping[key]
                data[key] = callback(dbentry)
            else:
                dbattr = self.formmapping[key]
                if dbattr == '__skip__':
                    continue
                data[key] = getattr(dbentry, dbattr)
                if self.null2emptystring and data[key] == None:
                    data[key] = ''

        if nesteddata:
            return data.to_dict()
        else:
            return data

    def set_dbrow(self, inrow, dbrow):
        """
        update database entry from form entry

        :param inrow: input row
        :param dbrow: database entry (model object)
        """
        for dbattr in self.dbmapping:
            if hasattr(self.dbmapping[dbattr], '__call__'):
                callback = self.dbmapping[dbattr]
                setattr(dbrow, dbattr, callback(inrow))
            else:
                key = self.dbmapping[dbattr]
                if key in inrow:
                    setattr(dbrow, dbattr, inrow[key])
                    if self.null2emptystring:
                        if getattr(dbrow, dbattr) == '':
                            setattr(dbrow, dbattr, None)


class TablesCsv(MethodView):
    __doc__ = "\n    provides flask render for csv.DictReader-like datasource as table\n\n    usage:\n        class yourDatatablesCsv(TablesCsv):\n            # overridden methods\n        instancename = yourDatatablesCsv([arguments]):\n        instancename.register()\n\n    see below for methods which must be overridden when subclassing\n\n    **columns** should be like the following. See https://datatables.net/reference/option/columns and \n    https://editor.datatables.net/reference/option/fields for more information\n\n        [\n            { 'data': 'name', 'name': 'name', 'label': 'Service Name' },\n            { 'data': 'key', 'name': 'key', 'label': 'Key' }, \n            { 'data': 'secret', 'name': 'secret', 'label': 'Secret', 'render':'$.fn.dataTable.render.text()' },\n        ]\n\n        * name - describes the column and is used within javascript\n        * data - used on server-client interface \n        * label - used for the DataTable table column. CSV file headers must match this\n        * optional render key is eval'd into javascript\n    \n    :param app: flask app this is running under\n    :param endpoint: endpoint parameter used by flask.url_for()\n    :param rule: rule parameter used by flask.add_url_rule() [defaults to '/' + endpoint]\n    "

    def open(self):
        """
        open source of "csv" data
        """
        raise NotImplementedError

    def nexttablerow(self):
        """
        return next record, similar to csv.DictReader - raises StopIteration
        :rtype: dict with row data for table
        """
        raise NotImplementedError

    def close(self):
        """
        close source of "csv" data
        """
        raise NotImplementedError

    def permission(self):
        """
        check for readpermission on data
        :rtype: boolean
        """
        raise NotImplementedError
        return False

    def renderpage(self, tabledata):
        """
        renders flask template with appropriate parameters
        :param tabledata: list of data rows for rendering
        :rtype: flask.render_template()
        """
        raise NotImplementedError

    def rollback(self):
        """
        any processing which must be done on page abort or exception
        """
        raise NotImplementedError

    def beforeget(self):
        """
        any processing which needs to be done at the beginning of the get
        """
        pass

    def abort(self):
        """
        any processing which needs to be done to abort when forbidden (e.g., redirect)
        """
        flask.abort(403)

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        args = dict(app=None, endpoint=None,
          rule=None)
        args.update(kwargs)
        args['rule'] = args['rule'] or '/' + args['endpoint']
        for key in args:
            setattr(self, key, args[key])

    def register(self):
        name = self.endpoint.split('.')[(-1)]
        my_view = (self.as_view)(name, **self.kwargs)
        self.app.add_url_rule(('{}'.format(self.rule)), view_func=my_view, methods=['GET'])

    def get(self):
        try:
            redirect = self.beforeget()
            if redirect:
                return redirect
            if not self.permission():
                self.rollback()
                self.abort()
            self.open()
            tabledata = []
            try:
                while True:
                    datarow = self.nexttablerow()
                    tabledata.append(datarow)

            except StopIteration:
                self.close()

            return self.renderpage(tabledata)
        except:
            self.rollback()
            raise


def _editormethod(checkaction='', formrequest=True):
    """
    decorator for CrudApi methods used by Editor

    :param methodcore: function() containing core of method to execute
    :param checkaction: Editor name of action which is used by the decorated method, one of 'create', 'edit', 'remove' or '' if no check required (can be list)
    :param formrequest: True if request action, data is in form (False for 'remove' action)
    """
    if debug:
        print('_editormethod(checkaction={}, formrequest={})'.format(checkaction, formrequest))

    def wrap(f):

        def wrapped_f(self, *args, **kwargs):
            redirect = self.init()
            if redirect:
                return redirect
            self._error = ''
            self._fielderrors = []
            try:
                if not self.permission():
                    self.rollback()
                    cause = 'operation not permitted for user'
                    return dt_editor_response(error=cause)
                else:
                    self.editor_method_prehook(request.form)
                    if formrequest:
                        action = get_request_action(request.form)
                        self._data = get_request_data(request.form)
                    else:
                        action = request.args['action']
                    if debug:
                        print('checkaction = {}'.format(checkaction))
                    if checkaction:
                        actioncheck = checkaction.split(',')
                    if checkaction:
                        if action not in actioncheck:
                            self.rollback()
                            cause = 'unknown action "{}"'.format(action)
                            current_app.logger.warning(cause)
                            return dt_editor_response(error=cause)
                self.beforequery()
                f(self, *args, **kwargs)
                self.editor_method_posthook(request.form)
                self.commit()
                return dt_editor_response(data=(self._responsedata))
            except:
                self.rollback()
                if self._fielderrors:
                    cause = 'please check indicated fields'
                else:
                    if self._error:
                        cause = self._error
                    else:
                        cause = traceback.format_exc()
                        current_app.logger.error(traceback.format_exc())
                return dt_editor_response(data=[], error=cause, fieldErrors=(self._fielderrors))

        return wrapped_f

    return wrap


class CrudApi(MethodView):
    __doc__ = "\n    provides initial render and RESTful CRUD api\n\n    usage:\n        instancename = CrudApi([arguments]):\n        instancename.register()\n\n    **dbmapping** is dict like {'dbattr_n':'formfield_n', 'dbattr_m':f(form), ...}\n    **formmapping** is dict like {'formfield_n':'dbattr_n', 'formfield_m':f(dbrow), ...}\n    if order of operation is important for either of these use OrderedDict\n\n    **clientcolumns** should be like the following. See https://datatables.net/reference/option/columns and \n    https://editor.datatables.net/reference/option/fields for more information\n\n        [\n            { 'data': 'name', 'name': 'name', 'label': 'Service Name' },\n            { 'data': 'key', 'name': 'key', 'label': 'Key', 'render':'$.fn.dataTable.render.text()' }, \n            { 'data': 'secret', 'name': 'secret', 'label': 'Secret', 'render':'$.fn.dataTable.render.text()' },\n            { 'data': 'service', 'name': 'service_id', \n              'label': 'Service Name',\n              'type': 'selectize', \n              'options': [{'label':'yes', 'value':1}, {'label':'no', 'value':0}],\n              'opts': { \n                'searchField': 'label',\n                'openOnFocus': False\n               },\n               'dt': { options for DataTables only }\n               'ed': { options for Editor only }\n              '_update': [see below]\n            },\n        ]\n\n        * name - describes the column and is used within javascript\n        * data - used on server-client interface and should be used in the formmapping key and dbmapping value\n        * label - used for the DataTable table column and the Editor form label \n        * render - (optional) is eval'd into javascript\n        * id - is specified by idSrc, and should be in the mapping function but not columns\n        * see https://datatables.net/reference/option/ (Columns) and https://editor.datatables.net/reference/option/ (Field) for more options\n\n        NOTE: for options which are supported by both DataTables and Editor, options may be configured only within\n        'dt' or 'ed' respectively to force being used for only that package, e.g., 'ed': {'render' ...} would render \n        just for the Editor, but be ignored for DataTables.\n\n        additionally the update option can be used to _update the options for any type = 'select', 'select2', selectize'\n\n        * _update - dict with following keys\n            * endpoint - url endpoint to retrieve new options \n            * on - event which triggers update. supported events are\n                * 'open' - triggered when form opens (actually when field is focused)\n                * 'change' - triggered when field changes - use wrapper to indicate what field(s) are updated\n            * wrapper - dict which is wrapped around query response. value '_response_' indicates where query response should be placed\n    \n                        OR\n\n        * _update - dict with the following keys\n                'options' : function() to retrieve option tree:\n                        {'val1':<val1 Return options / JSON>,\n                         'val2':<val2 Return options / JSON>,\n                         ...}\n                    when this field changes to 'val1', val1 Return options / JSON fetched and handled by Editor\n                    see https://editor.datatables.net/reference/api/dependent(), Return options / JSON\n              }\n\n    **serverside** - if true table will be displayed through ajax get calls\n\n    **scriptfilter** - can be used to filter list of scripts into full pathname, version argument, etc\n\n    :param app: flask app or blueprint\n    :param pagename: name to be displayed at top of html page\n    :param endpoint: endpoint parameter used by flask.url_for()\n    :param endpoint_values: values dict for endpoint, default {}, substitution as _value_, e.g., {'value':'_value_'}\n        this can be used for permission grouping in url, e.g., /admin/_value_/endpoint\n    :param rule: rule parameter used by flask.add_url_rule() [defaults to '/' + endpoint]\n    :param eduploadoption: editor upload option (optional) see https://editor.datatables.net/reference/option/ajax\n    :param clientcolumns: list of dicts for input to dataTables and Editor\n    :param filtercoloptions: list of clientcolumns options which are to be filtered out\n    :param serverside: set to true to use ajax to get table data\n    :param idSrc: idSrc for use by Editor\n    :param buttons: list of buttons for DataTable, from ['create', 'remove', 'edit', 'csv']\n    :param pretablehtml: string any html which needs to go before the table\n\n    :param scriptfilter: function to filter pagejsfiles and pagecssfiles lists into full path / version lists\n    :param dtoptions: dict of datatables options to apply at end of options calculation\n    :param edoptions: dict of datatables editor options to apply at end of options calculation\n    :param yadcfoptions: dict of yadcf options to apply at end of options calculation\n    :param pagejsfiles: list of javascript file paths to be included\n    :param pagecssfiles: list of css file paths to be included\n    :param templateargs: dict of arguments to pass to template - if callable arg function is called before being passed to template (no parameters)\n    :param validate: editor validation function (action, formdata), result is set to self._fielderrors\n    :param multiselect: if True, allow selection of multiple rows, default False\n    "

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        args = dict(app=None, template='datatables.html',
          pagename=None,
          endpoint=None,
          endpointvalues={},
          rule=None,
          eduploadoption=None,
          clientcolumns=None,
          filtercoloptions=[],
          serverside=False,
          files=None,
          idSrc='DT_RowId',
          buttons=[
         'create', 'edit', 'remove', 'csv'],
          pretablehtml='',
          scriptfilter=(lambda filelist: filelist),
          dtoptions={},
          edoptions={},
          yadcfoptions={},
          pagejsfiles=[],
          pagecssfiles=[],
          templateargs={},
          validate=(lambda action, formdata: []),
          multiselect=False,
          addltemplateargs={})
        args.update(kwargs)
        args['rule'] = args['rule'] or '/' + args['endpoint']
        for key in args:
            setattr(self, key, args[key])

    def register(self):
        name = self.endpoint.split('.')[(-1)]
        self.my_view = (self.as_view)(name, **self.kwargs)
        self.app.add_url_rule(('{}'.format(self.rule)), view_func=(self.my_view), methods=['GET'])
        self.app.add_url_rule(('{}/rest'.format(self.rule)), view_func=(self.my_view), methods=['GET', 'POST'])
        self.app.add_url_rule(('{}/rest/<int:thisid>'.format(self.rule)), view_func=(self.my_view), methods=['PUT', 'DELETE'])
        if self.files:
            self.files.register()
            if debug:
                print('self.files.register()')

    def _renderpage(self):
        try:
            redirect = self.init()
            if redirect:
                return redirect
            if not self.permission():
                self.rollback()
                self.abort()
            self.beforequery()
            update_options = []
            for column in self.clientcolumns:
                if '_update' in column:
                    update = column['_update']
                    if 'url' in update:
                        update['url'] = url_for(update['endpoint']) + '?' + urlencode({'_wrapper': dumps(update['wrapper'])})
                        update['name'] = column['name']
                        update_options.append(update)
                    else:
                        if 'options' in update:
                            thisupdate = {}
                            if 'ed' in column:
                                if 'name' in column['ed']:
                                    thisupdate['name'] = column['ed']['name']
                            else:
                                thisupdate['name'] = column['name']
                            thisupdate['options'] = update['options']()
                            update_options.append(thisupdate)
                        else:
                            raise ParameterError('invalid _update format: {}'.format(update))

            dt_options = self.getdtoptions()
            ed_options = self.getedoptions()
            yadcf_options = self.getyadcfoptions()
            if not self.serverside:
                self.open()
                tabledata = []
                try:
                    while True:
                        thisentry = self.nexttablerow()
                        tabledata.append(thisentry)

                except StopIteration:
                    pass

                self.close()
            else:
                tabledata = '{}/rest'.format(url_for(self.endpoint))
            if self.files:
                tablefiles = self.files.list()
                if debug:
                    print(tablefiles)
            else:
                tablefiles = None
            self.commit()
            return (self.render_template)(pagename=self.pagename, pagejsfiles=self.scriptfilter(self.pagejsfiles), 
             pagecssfiles=self.scriptfilter(self.pagecssfiles), 
             tabledata=tabledata, 
             tablefiles=tablefiles, 
             tablebuttons=self.buttons, 
             pretablehtml=self.pretablehtml, 
             options={'dtopts':dt_options, 
 'editoropts':ed_options, 
 'yadcfopts':yadcf_options, 
 'updateopts':update_options}, 
             writeallowed=self.permission(), **self.addltemplateargs)
        except:
            self.rollback()
            raise

    def _retrieverows(self):
        try:
            redirect = self.init()
            if redirect:
                return redirect
            else:
                if not self.permission():
                    self.rollback()
                    self.abort()
                self.beforequery()
                self.open()
                tabledata = []
                try:
                    while True:
                        thisentry = self.nexttablerow()
                        tabledata.append(thisentry)

                except StopIteration:
                    pass

                self.close()
                if hasattr(self, 'output_result'):
                    return jsonify(self.output_result)
                output_result = tabledata
                return jsonify(output_result)
        except:
            self.rollback()
            raise

    def getdtoptions(self):
        dt_options = {'dom':'<"H"lBpfr>t<"F"i>', 
         'columns':[
          {'data':None, 
           'defaultContent':'', 
           'className':'select-checkbox', 
           'orderable':False}], 
         'rowId':self.idSrc, 
         'select':'single' if not self.multiselect else 'os', 
         'ordering':True, 
         'order':[
          1, 'asc']}
        for column in self.clientcolumns:
            if 'edonly' in column:
                pass
            else:
                dtcolumn = {key:(column[key] if not callable(column[key]) else column[key]()) for key in column if key not in self.filtercoloptions + ['dtonly']}
                dtspecific = dtcolumn.pop('dt', {})
                dtcolumn.pop('ed', {})
                dtcolumn.pop('_update', {})
                dtcolumn.update(dtspecific)
                dt_options['columns'].append(dtcolumn)

        dt_options['serverSide'] = self.serverside
        dt_options.update(self.dtoptions)
        return dt_options

    def getedoptions(self):
        ed_options = {'idSrc':self.idSrc, 
         'ajax':{'create':{'type':'POST', 
           'url':'{}/rest'.format(url_for((self.endpoint), **self.endpointvalues))}, 
          'edit':{'type':'PUT', 
           'url':'{}/rest/{}'.format(url_for((self.endpoint), **self.endpointvalues), '_id_')}, 
          'editRefresh':{'type':'PUT', 
           'url':'{}/rest'.format(url_for((self.endpoint), **self.endpointvalues))}, 
          'remove':{'type':'DELETE', 
           'url':'{}/rest/{}'.format(url_for((self.endpoint), **self.endpointvalues), '_id_')}}, 
         'fields':[]}
        fieldkeys = [
         'className', 'data', 'def', 'entityDecode', 'fieldInfo', 'id', 'label', 'labelInfo', 'name', 'type', 'options', 'opts', 'ed', 'separator', 'dateFormat', 'onFocus']
        for column in self.clientcolumns:
            if 'dtonly' in column:
                pass
            else:
                edcolumn = {key:(column[key] if not callable(column[key]) else column[key]()) for key in fieldkeys if key not in self.filtercoloptions + ['edonly']}
                edspecific = edcolumn.pop('ed', {})
                edcolumn.update(edspecific)
                ed_options['fields'].append(edcolumn)

        if self.eduploadoption:
            ed_options['ajax']['upload'] = self.eduploadoption
        ed_options.update(self.edoptions)
        if debug:
            current_app.logger.debug('getedoptions(): ed_options={}'.format(ed_options))
        return ed_options

    def getyadcfoptions(self):
        return self.yadcfoptions

    def get(self):
        print('request.path = {}'.format(request.path))
        if request.path[-5:] != '/rest':
            return self._renderpage()
        else:
            return self._retrieverows()

    @_editormethod(checkaction='create,refresh', formrequest=True)
    def post(self):
        thisdata = self._data[0]
        action = get_request_action(request.form)
        self._fielderrors = self.validate(action, thisdata)
        if self._fielderrors:
            raise ParameterError
        else:
            if action == 'create':
                thisrow = self.createrow(thisdata)
                self._responsedata = [thisrow]
            else:
                if action == 'refresh':
                    form = request.form
                    if 'refresh' in form:
                        if 'ids' in form:
                            self._responsedata = self.refreshrows(form['ids'])
                    cause = 'post(): edit action without refresh parameters'
                    current_app.logger.error(cause)
                    self._error = cause
                    raise ParameterError(cause)
                else:
                    thisrow = self.upload(thisdata)

    @_editormethod(checkaction='edit', formrequest=True)
    def put(self, thisid):
        self._responsedata = []
        thisdata = self._data[thisid]
        self._fielderrors = self.validate('edit', thisdata)
        if self._fielderrors:
            raise ParameterError
        thisrow = self.updaterow(thisid, thisdata)
        self._responsedata = [
         thisrow]

    @_editormethod(checkaction='remove', formrequest=False)
    def delete(self, thisid):
        self.deleterow(thisid)
        self._responsedata = []

    def open(self):
        """
        open source of "csv" data
        """
        raise NotImplementedError

    def nexttablerow(self):
        """
        return next record, similar to csv.DictReader - raises StopIteration
        :rtype: dict with row data for table
        """
        raise NotImplementedError

    def close(self):
        """
        close source of "csv" data
        """
        raise NotImplementedError

    def permission(self):
        """
        check for readpermission on data
        :rtype: boolean
        """
        raise NotImplementedError
        return False

    def createrow(self, formdata):
        """
        creates row in database
        
        :param formdata: data from create form
        :rtype: returned row for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        raise NotImplementedError

    def refreshrows(self, ids):
        """
        refreshes rows from database
        
        :param ids: comma separated ids for which refresh is required
        :rtype: returned rows for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        current_app.logger.debug('tables.refreshrows("{}"): reached'.format(ids))
        raise NotImplementedError

    def updaterow(self, thisid, formdata):
        """
        updates row in database
        
        :param thisid: id of row to be updated
        :param formdata: data from create form
        :rtype: returned row for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        raise NotImplementedError

    def deleterow(self, thisid):
        """
        deletes row in database
        
        :param thisid: id of row to be updated
        :rtype: returned row for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        raise NotImplementedError

    def init(self):
        """
        optional return redirect URL
        :return: redirect url or None if no redirect
        """
        pass

    def beforequery(self):
        """
        update self.queryparams if necessary
        """
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def abort(self):
        flask.abort(403)

    def render_template(self, **kwargs):
        theseargs = {}
        current_app.logger.debug('rendertemplate(): self.templateargs = {}'.format(self.templateargs))
        for arg in self.templateargs:
            current_app.logger.debug('rendertemplate(): adding {} to template args'.format(arg))
            if callable(self.templateargs[arg]):
                theseargs[arg] = self.templateargs[arg]()
            else:
                theseargs[arg] = self.templateargs[arg]

        theseargs.update(kwargs)
        return (flask.render_template)((self.template), **theseargs)

    def editor_method_prehook(self, form):
        """
        This method is called within post() [create], put() [edit], delete() [edit] after permissions are checked

        Replace this if any preprocessing is required based on the form. The form itself cannot be changed

        NOTE: any updates to form validation should be done in self.validation()

        parameters:
        * form - request.form object (immutable)
        """
        pass

    def editor_method_posthook(self, form):
        """
        This method is called within post() [create], put() [edit], delete() [edit] db commit() just before database
        commit and response to client

        Use get_request_action(form) to determine which method is in progress
        self._responsedata has data about to be returned to client

        parameters:
        * form - request.form object (immutable)
        """
        pass


def _uploadmethod():
    """
    decorator for CrudFiles methods used by Editor

    :param methodcore: function() containing core of method to execute
    """

    def wrap(f):

        def wrapped_f(self, *args, **kwargs):
            try:
                f(self, *args, **kwargs)
                return dt_editor_response(**self._responsedata)
            except Exception as e:
                cause = 'Unexpected Error: {}\n{}'.format(e, traceback.format_exc())
                current_app.logger.error(cause)
                return dt_editor_response(error=cause)

        return wrapped_f

    return wrap


class DteDbRelationship:
    __doc__ = '\n    define relationship for datatables editor db - form interface\n\n    for relationships defined like\n    class model()\n        dbfield            = relationship( \'mappingmodel\', backref=tablemodel, lazy=True )\n\n    * tablemodel - name of model for the table\n    * fieldmodel - name of model comprises list in dbfield\n    * labelfield - field in model which is used to be displayed to the user\n    * valuefield - field in model which is used as value for select and to retrieve record, passed on Editor interface, default \'id\' - needs to be a key for model record\n    * formfield - field as used on the form\n    * dbfield - field as used in the database table (not the model -- this is field in table which has list of model items)\n    * uselist - set to True if using tags, otherwise field expects single entry, default True\n    * searchbox - set to True if searchbox desired, default False\n    * nullable - set to True if item can give null (unselected) return, default False (only applies for usellist=False)\n    * queryparams - dict containing parameters for query to determine options, or callable which returns such a dict\n\n    e.g.,\n        class Parent(Base):\n            __tablename__ = \'parent\'\n            id = Column(Integer, primary_key=True)\n            child_id = Column(Integer, ForeignKey(\'child.id\'))\n            child = relationship("Child", backref="parents")\n\n        class Child(Base):\n            __tablename__ = \'child\'\n            name = Column(String)\n            id = Column(Integer, primary_key=True)\n\n        TODO: add more detail here -- this is confusing\n\n        children = DteDbRelationship(tablemodel=Parent, fieldmodel=Child, labelfield=\'name\', formfield=\'children\', dbfield=\'children\')\n    '

    def __init__(self, **kwargs):
        args = dict(tablemodel=None, fieldmodel=None,
          labelfield=None,
          valuefield='id',
          formfield=None,
          dbfield=None,
          uselist=True,
          searchbox=False,
          nullable=False,
          queryparams={})
        args.update(kwargs)
        reqdfields = [
         'fieldmodel', 'labelfield', 'formfield', 'dbfield']
        for field in reqdfields:
            if not args[field]:
                raise ParameterError('{} parameters are all required'.format(', '.join(reqdfields)))

        for key in args:
            setattr(self, key, args[key])

    def set(self, formrow):
        if self.uselist:
            items = []
            itemvalues = []
            for key in formrow[self.formfield]:
                vallist = formrow[self.formfield][key].split(SEPARATOR)
                if len(vallist) == 1:
                    if not vallist[0]:
                        continue
                for ndx in range(len(vallist)):
                    if len(itemvalues) < ndx + 1:
                        itemvalues.append({key: vallist[ndx]})
                    else:
                        itemvalues[ndx].update({key: vallist[ndx]})

            if debug:
                current_app.logger.debug('itemvalues={}'.format(itemvalues))
            for itemvalue in itemvalues:
                queryfilter = itemvalue
                thisitem = (self.fieldmodel.query.filter_by)(**queryfilter).one()
                items.append(thisitem)

            return items
        else:
            itemvalue = formrow[self.formfield] if formrow[self.formfield] else None
            queryfilter = itemvalue
            thisitem = (self.fieldmodel.query.filter_by)(**queryfilter).one_or_none()
            return thisitem

    def get(self, dbrow_or_id):
        if type(dbrow_or_id) in [int, str]:
            dbrow = self.tablemodel.query().filter_by(id=dbrow_or_id).one()
        else:
            dbrow = dbrow_or_id
        if self.uselist:
            items = {}
            labelitems = []
            valueitems = []
            for item in getattr(dbrow, self.dbfield):
                labelitems.append(str(getattr(item, self.labelfield)))
                valueitems.append(str(getattr(item, self.valuefield)))

            items = {self.labelfield: SEPARATOR.join(labelitems), self.valuefield: SEPARATOR.join(valueitems)}
            return items
        else:
            if getattr(dbrow, self.dbfield):
                item = {self.labelfield: getattr(getattr(dbrow, self.dbfield), self.labelfield), 
                 self.valuefield: getattr(getattr(dbrow, self.dbfield), self.valuefield)}
                return item
            return {self.labelfield: None, self.valuefield: None}

    def options(self):
        queryparams = self.queryparams() if callable(self.queryparams) else self.queryparams
        items = []
        if self.nullable:
            items += [{'label':'<none>',  'value':None}]
        items += [{'label':getattr(item, self.labelfield),  'value':item.id} for item in (self.fieldmodel.query.filter_by)(**queryparams).all()]
        items.sort(key=(lambda k: k['label'].lower()))
        return items

    def new_plus_options(self):
        items = [
         {'label':'<new>', 
          'value':0}] + self.options()
        return items


class DteDbSubrec:
    __doc__ = '\n    define subfield relationship for datatables editor db - form interface\n\n    for relationships defined like\n    class model()\n        field            = relationship( \'mappingmodel\', backref=tablemodel, lazy=True )\n\n    * model - model comprises the subrec\n    * dbfield - field in model which is used to be displayed to the user\n    * formfield - field name on form associated with this db field\n\n    e.g.,\n        class Parent(Base):\n            __tablename__ = \'parent\'\n            id = Column(Integer, primary_key=True)\n            child_id = Column(Integer, ForeignKey(\'child.id\'))\n            child = relationship("Child", backref="parents")\n\n        class Child(Base):\n            __tablename__ = \'child\'\n            name = Column(String)\n            id = Column(Integer, primary_key=True)\n\n        TODO: add more detail here -- this is confusing\n\n        reln = DteDbSubrec(model=Child, dbfield=\'name\', formfield=\'name\')\n    '

    def __init__(self, **kwargs):
        args = dict(model=None, field=None,
          subfield=None,
          formfield=None)
        args.update(kwargs)
        reqdfields = [
         'model', 'field', 'subfield', 'formfield']
        for field in reqdfields:
            if not args[field]:
                raise ParameterError('{} parameters are all required'.format(', '.join(reqdfields)))

        for key in args:
            setattr(self, key, args[key])

    def set(self, formrow):
        itemvalue = formrow[self.formfield] if formrow[self.formfield] else None
        queryfilter = itemvalue
        thisitem = (self.model.query.filter_by)(**queryfilter).one_or_none()
        return thisitem

    def get(self, dbrow_or_id):
        if type(dbrow_or_id) in [int, str]:
            dbrow = self.model.query().filter_by(id=dbrow_or_id).one()
        else:
            dbrow = dbrow_or_id
        if getattr(dbrow, self.field):
            item = getattr(getattr(dbrow, self.field), self.subfield)
            return item
        else:
            return


class DteDbBool:
    __doc__ = "\n    define helpers for boolean fields\n\n    * formfield - field as used on the form\n    * dbfield - field as used in the database\n    * truedisplay - how to display True to user (default 'yes')\n    * falsedisplay - hot to display False to user (default 'no')\n    "

    def __init__(self, **kwargs):
        args = dict(tablemodel=None, formfield=None,
          dbfield=None,
          truedisplay='yes',
          falsedisplay='no')
        args.update(kwargs)
        reqdfields = [
         'formfield', 'dbfield']
        for field in reqdfields:
            if not args[field]:
                raise ParameterError('{} parameters are all required'.format(', '.join(reqdfields)))

        for key in args:
            setattr(self, key, args[key])

    def get(self, dbrow_or_id):
        """get from database for form"""
        if type(dbrow_or_id) in [int, str]:
            dbrow = self.tablemodel.query().filter_by(id=dbrow_or_id).one()
        else:
            dbrow = dbrow_or_id
        if getattr(dbrow, self.dbfield):
            return self.truedisplay
        else:
            return self.falsedisplay

    def sqla_expr(self):
        """
        get from database when using serverside = True, for use with ColumnDT

        :return: sqlalchemy expression
        """
        return renderboolean((get_dbattr(self.tablemodel, self.dbfield)),
          truedisplay=(self.truedisplay),
          falsedisplay=(self.falsedisplay))

    def set(self, formrow):
        """set to database from form"""
        return formrow[self.formfield] == self.truedisplay

    def options(self):
        return [
         {'label':self.truedisplay, 
          'value':self.truedisplay},
         {'label':self.falsedisplay, 
          'value':self.falsedisplay}]


class DteDbDependent:
    __doc__ = '\n    define dependent options between fields\n\n    * model - which when changed uses options from dependent model\n    * modelfield - field within model to drive changes in dependent model - default \'id\'\n    * depmodel - dependent model\n    * depmodelref - field which refers back to model\n    * depmodelfield - field in dependent model which are displayed to user\n    * depvaluefield - field in dependent model which is used as value for select and to retrieve record, passed on Editor interface\n        default \'id\' - needs to be a key for model record\n\n    e.g.,\n        class Parent(Base):\n            __tablename__ = \'parent\'\n            id = Column(Integer, primary_key=True)\n            child_id = Column(Integer, ForeignKey(\'child.id\'))\n            child = relationship("Child", backref="parent")\n\n        class Child(Base):\n            __tablename__ = \'child\'\n            name = Column(String)\n            id = Column(Integer, primary_key=True)\n            parent_id = Column( Integer, ForeignKey(\'parent.id\') )\n            parent    = relationship( \'Parent\', backref=\'children\', lazy=True )\n\n        TODO: add more detail here -- this is confusing\n\n        children = DteDbDependent(model=Parent,\n                                  modelfield=\'id\',\n                                  depmodel=Child,\n                                  depmodelref=\'parent\',\n                                  depmodelfield=\'name\',\n                                  depformfield=\'formfieldname\',\n                                  depvaluefield=\'id\',\n                                 )\n\n        children is callable function which returns tree suitable for tables.CrudApi _update.options\n    '

    def __init__(self, **kwargs):
        args = dict(model=None, modelfield='id',
          depmodel=None,
          defmodelref=None,
          depmodelfield=None,
          depformfield=None,
          depvaluefield='id')
        args.update(kwargs)
        reqdfields = [
         'model', 'modelfield', 'depmodel', 'depmodelfield', 'depvaluefield']
        for field in reqdfields:
            if not args[field]:
                raise ParameterError('{} parameters are all required'.format(', '.join(reqdfields)))

        for key in args:
            setattr(self, key, args[key])

    def __call__(self):
        dbvals = self.model.query.all()
        vals = [getattr(v, self.modelfield) for v in dbvals]
        retoptions = {}
        for val in vals:
            retoptions[val] = {'options': {}}
            formoptions = retoptions[val]['options'][self.depformfield] = []
            query = {self.depmodelref: val}
            dbopts = (self.depmodel.query.filter_by)(**query).all()
            for dbopt in dbopts:
                formoptions.append({'label':getattr(dbopt, self.depmodelfield),  'value':getattr(dbopt, self.depvaluefield)})

        return retoptions


class DbCrudApi(CrudApi):
    __doc__ = "\n    This class extends CrudApi. This extension uses sqlalchemy to read / write to a database\n\n    Additional parameters for this class:\n\n        db: database object a la sqlalchemy\n        model: sqlalchemy model for the table to read/write from\n        dbmapping: mapping dict with key for each db field, value is key in form or function(dbentry)\n        formmapping: mapping dict with key for each form row, value is key in db row or function(form)\n        queryparams: dict of query parameters relevant to this table to retrieve table or rows\n        dtoptions: datatables options to override / add\n        version_id_col: name of column which contains version id\n        checkrequired: True causes checks of columns with className: 'field_req'\n\n        **dbmapping** is dict like {'dbattr_n':'formfield_n', 'dbattr_m':f(form), ...}\n        **formmapping** is dict like {'formfield_n':'dbattr_n', 'formfield_m':f(dbrow), ...}\n        if order of operation is important for either of these use OrderedDict\n\n        **clientcolumns** should be like the following. See https://datatables.net/reference/option/columns and\n        https://editor.datatables.net/reference/option/fields for more information\n            [\n                { 'data': 'service', 'name': 'service', 'label': 'Service Name' },\n                { 'data': 'key', 'name': 'key', 'label': 'Key', 'render':'$.fn.dataTable.render.text()' },\n                { 'data': 'secret', 'name': 'secret', 'label': 'Secret', 'render':'$.fn.dataTable.render.text()' },\n                { 'data': 'service', 'name': 'service_id',\n                  'label': 'Service Name',\n                  'type': 'selectize',\n                  'options': [{'label':'yes', 'value':1}, {'label':'no', 'value':0}],\n                  'opts': {\n                    'searchField': 'label',\n                    'openOnFocus': False\n                   },\n                  '_update' {\n                    'endpoint' : <url endpoint to retrieve options from>,\n                    'on' : <event>\n                    'wrapper' : <wrapper for query response>\n                  }\n                },\n            ]\n            * name - describes the column and is used within javascript\n            * data - used on server-client interface and should be used in the formmapping key and dbmapping value\n            * label - used for the DataTable table column and the Editor form label\n            * optional render key is eval'd into javascript\n            * id - is specified by idSrc, and should be in the mapping function but not columns\n\n            additionally the update option can be used to _update the options for any type = 'select', 'selectize'\n            * _update - dict with following keys\n                * endpoint - url endpoint to retrieve new options\n                * on - event which triggers update. supported events are\n                    * 'open' - triggered when form opens (actually when field is focused)\n                    * 'change' - triggered when field changes - use wrapper to indicate what field(s) are updated\n                * wrapper - dict which is wrapped around query response. value '_response_' indicates where query response should be placed\n\n            * _treatment - dict with (only) one of following keys - note this causes override of dbmapping and formmapping configuration\n                * boolean - {DteDbBool keyword parameters}\n                * relationship - {DteDbRelationship keyword parameters, 'editable' : { 'api':<DbCrudApi()> }}\n                    'editable' is set only if it is desired to bring up a form to edit the underlying model row\n\n            * _ColumnDT_args - dict with keyword arguments passed to ColumnDT for serverside processing\n\n        **serverside** - if present table will be displayed through ajax get calls\n\n        **version_id_col** - if present edits to this table are protected using optimistic concurrency control\n          * see https://en.wikipedia.org/wiki/Optimistic_concurrency_control\n          * also https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html\n          * this column is automaticalled added to dbmapping, formmapping and clientcolumns\n          * e.g., for version_id_col='version_id', database model for this table should have code like\n                ```\n                version_id          = Column(Integer, nullable=False)\n                __mapper_args__ = {\n                    'version_id_col' : version_id\n                }\n                ```\n    "

    def __init__(self, **kwargs):
        if debug:
            current_app.logger.debug('DbCrudApi.__init__()')
        else:
            args = dict(db=None, model=None,
              dbmapping={},
              formmapping={},
              version_id_col=None,
              serverside=False,
              queryparams={},
              dtoptions={},
              filtercoloptions=[],
              checkrequired=None)
            args.update(kwargs)
            args['filtercoloptions'] += ['_treatment', '_unique', '_ColumnDT_args']
            self.formmapping = deepcopy(args['formmapping'])
            self.dbmapping = deepcopy(args['dbmapping'])
            self.uniquecols = []
            version_id_col = args['version_id_col']
            if version_id_col:
                self.occupdate = False
                self.formmapping[version_id_col] = version_id_col
                self.dbmapping[version_id_col] = lambda form: int(form['version_id']) if form['version_id'] else 0
                versioncol = {'name':version_id_col, 
                 'data':version_id_col, 
                 'ed':{'type': 'hidden'}, 
                 'dt':{'visible': False}}
                if version_id_col not in [c['name'] for c in args['clientcolumns']]:
                    args['clientcolumns'].append(versioncol)
            if args['serverside']:
                self.servercolumns = [
                 ColumnDT((getattr(args['model'], 'id')), mData=(self.dbmapping['id']))]
            booleandb = {}
            booleanform = {}
            self.saforms = []
            for col in args['clientcolumns']:
                if debug:
                    current_app.logger.debug('__init__(): col = {}'.format(col))
                else:
                    if col.get('type', None) == 'readonly':
                        self.dbmapping.pop(col['name'], None)
                    formfield = col['name']
                    dbattr = self.formmapping[formfield]
                    if col.get('_unique', False):
                        self.uniquecols.append(dbattr)
                    treatment = col.get('_treatment', None)
                    columndt_args = col.get('_ColumnDT_args', {})
                    if debug:
                        current_app.logger.debug('__init__(): treatment = {}'.format(treatment))
                if not treatment:
                    if args['serverside']:
                        self.servercolumns.append(ColumnDT(getattr(args['model'], dbattr), mData=formfield, **columndt_args))
                    if not callable(dbattr):
                        branches = dbattr.split('.')
                        if len(branches) == 2:
                            submodelname = branches[0]
                            submodel = type(getattr(args['model'], submodelname))
                            subfield = branches[1]
                            thisreln = DteDbSubrec(model=submodel, field=submodelname, subfield=subfield, formfield=formfield)
                            if not args['serverside']:
                                self.formmapping[formfield] = thisreln.get
                            else:
                                self.servercolumns.append(ColumnDT(thisreln.get(getattr(submodel, 'id')), mData=formfield, **columndt_args))
                            self.dbmapping[dbattr] = '__readonly__'
                            col['type'] = 'readonly'
                else:
                    if not isinstance(treatment, dict) or len(treatment) != 1 or list(treatment.keys())[0] not in ('boolean',
                                                                                                                   'relationship'):
                        raise ParameterError('invalid treatment: {}'.format(treatment))
                    if 'boolean' in treatment:
                        thisbool = DteDbBool(tablemodel=args['model'], **treatment['boolean'])
                        col['type'] = 'select2'
                        col['opts'] = {'minimumResultsForSearch': 'Infinity'}
                        booleanform[formfield] = thisbool
                        col['options'] = booleanform[formfield].options
                        if not args['serverside']:
                            self.formmapping[formfield] = booleanform[formfield].get
                        else:
                            self.servercolumns.append(ColumnDT(thisbool.sqla_expr(), mData=formfield, **columndt_args))
                        booleandb[dbattr] = thisbool
                        self.dbmapping[dbattr] = booleandb[dbattr].set
                    if 'relationship' in treatment:
                        thisreln = DteDbRelationship(tablemodel=args['model'], **treatment['relationship'])
                        col['type'] = 'select2'
                        col['onFocus'] = 'focus'
                        col['opts'] = {'minimumResultsForSearch':0 if thisreln.searchbox else 'Infinity',  'multiple':thisreln.uselist, 
                         'placeholder':None if thisreln.uselist else '(select)'}
                        if thisreln.uselist:
                            col['separator'] = SEPARATOR
                        if not args['serverside']:
                            self.formmapping[formfield] = thisreln.get
                        else:
                            self.servercolumns.append(ColumnDT(func.thisreln.get(getattr(thisreln.tablemodel, 'id')), mData=formfield, **columndt_args))
                        self.dbmapping[dbattr] = thisreln.set
                        editable = treatment['relationship'].get('editable', {})
                        if debug:
                            current_app.logger.debug('__init__(): labelfield={} editable={}'.format(treatment['relationship']['labelfield'], editable))
                        valuefield = 'id' if 'valuefield' not in treatment['relationship'] else treatment['relationship']['valuefield']
                        labelfield = treatment['relationship']['labelfield']
                        formfield = treatment['relationship']['formfield']
                        if editable:
                            self.saforms.append({'api':editable['api'],  'args':{'labelfield':labelfield, 
                              'valuefield':valuefield,  'parentfield':formfield}})
                            for saform in editable['api'].saforms:
                                thisform = saform
                                if 'parent' not in saform['args']:
                                    thisform = {}
                                    thisform['api'] = saform['api']
                                    thisform['args'] = copy(saform['args'])
                                    thisform['args']['parent'] = '{}_editor'.format(treatment['relationship']['labelfield'])
                                self.saforms.append(thisform)

                            col['options'] = thisreln.new_plus_options
                        else:
                            col['options'] = thisreln.options
                            col['options'] = thisreln.options
                        if 'data' in col:
                            col.setdefault('dt', {}).update({'data': '{}.{}'.format(col['data'], thisreln.labelfield)})
                            col.setdefault('ed', {}).update({'data': '{}.{}'.format(col['data'], thisreln.valuefield)})
                        if 'name' in col:
                            col.setdefault('dt', {}).update({'name': '{}.{}'.format(col['name'], thisreln.labelfield)})
                            col.setdefault('ed', {}).update({'name': '{}.{}'.format(col['name'], thisreln.valuefield)})

            self.dte = DataTablesEditor((self.dbmapping), (self.formmapping), null2emptystring=True)
            (super(DbCrudApi, self).__init__)(**args)
            if self.saforms:
                self.saformjsurls = lambda : [(saf['api'].saformurl)(**saf['args']) for saf in self.saforms]
                self.templateargs['saformjsurls'] = self.saformjsurls
            self.callervalidate = self.validate
            self.validate = self.validatedb
            if debug:
                current_app.logger.debug('updated validate() to validatedb()')

    def get(self):
        if request.path[-7:] == '/saform':
            edoptions = self.getedoptions()
            return jsonify({'edoptions': edoptions})
        else:
            if request.path[-9:] == '/saformjs':
                ed_options = self.getedoptions()
                edoptsjson = ['    {}'.format(l) for l in dumps(ed_options, indent=2).split('\n')]
                labelfield = request.args['labelfield']
                parentfield = request.args['parentfield']
                valuefield = request.args['valuefield']
                parent = request.args.get('parent', 'editor')
                js = [
                 'var {}_{}_lastval;'.format(parentfield, valuefield),
                 'var {}_editor;'.format(labelfield),
                 'if ( typeof editorstack == "undefined" ) {',
                 '    var editorstack = [];',
                 '    var curreditor = editor;',
                 '    var pushing = false;',
                 '    var restoring = false;',
                 '    var parentbuttons;',
                 '}',
                 '',
                 '$( function () {',
                 '  if ( editorstack.length == 0 ) {',
                 '      curreditor = editor;',
                 '      parentbuttons = [',
                 '                 {',
                 '                  label: "Cancel",',
                 '                  fn: function () {',
                 '                        this.close();',
                 '                  },',
                 '                 },',
                 '                 {',
                 '                  label: "Create",',
                 '                  fn: function () {',
                 '                        this.submit( );',
                 '                  },',
                 '                 },',
                 '      ];',
                 '  }',
                 '',
                 '  if ( typeof pusheditor == "undefined" ) {',
                 '      function pusheditor( neweditor, parentname, buttons, editorname ) {',
                 '        var fields = {};',
                 '        $.each(curreditor.fields(), function(i, field) {',
                 '            fields[field] = curreditor.field(field).get();',
                 '        });',
                 '        pushing = true;',
                 '        curreditor.close()',
                 '        pushing = false;',
                 '        editorstack.push( { editor:curreditor, newcurrent:editorname, fields:fields, buttons:parentbuttons.map(a => $.extend(true, {}, a)) } );',
                 '        parentbuttons = buttons;',
                 '        curreditor = neweditor;',
                 '      }',
                 '',
                 '      function popeditor( ) {',
                 '        editorrec = editorstack.pop();',
                 '        curreditor = editorrec.editor;',
                 '        buttons = editorrec.buttons;',
                 '          curreditor',
                 '            .buttons( buttons )',
                 '            .create();',
                 '          restoring = true;',
                 '          $.each(editorrec.fields, function(field, val) {',
                 '              curreditor.field(field).set( val );',
                 '          });',
                 '          restoring = false;',
                 '      }',
                 '  }',
                 '',
                 '  // handle save, then open parent on submit',
                 '  var fieldname = "{}.{}"'.format(labelfield, valuefield),
                 '  var parentname = "{}.{}"'.format(parentfield, valuefield),
                 '  var {label}_buttons = ['.format(label=labelfield),
                 '                 {',
                 '                  label: "Cancel",',
                 '                  fn: function () {',
                 '                        this.close();',
                 '                  },',
                 '                 },',
                 '                 {',
                 '                  label: "Create",',
                 '                  fn: function () {',
                 '                        this.submit( function(resp) {',
                 '                              var newval = {{label:resp.data[0].{}, value:resp.data[0].{}}};'.format(labelfield, self.idSrc),
                 '                              curreditor.field( parentname ).AddOption( [ newval ] );',
                 '                              curreditor.field( parentname ).set( newval.value );',
                 '                           },',
                 '                        )',
                 '                  },',
                 '                 },',
                 '                ];',
                 '  $( {}.field( parentname ).input() ).on ("select2:open", function () {{'.format(parent),
                 '    {}_{}_lastval = {}.get( parentname );'.format(parentfield, valuefield, parent),
                 '  } );',
                 '  $( {}.field( parentname ).input() ).on ("change", function (e) {{'.format(parent),
                 '    // only fire if <new> entry',
                 '    if ( {}.get( parentname ) != 0 ) return;'.format(parent),
                 '    // no fire if restoring',
                 '    if ( restoring ) return;',
                 '',
                 '    pusheditor( {label}_editor, parentname, {label}_buttons, "{label}_editor" );'.format(label=labelfield),
                 '',
                 '    {}_editor'.format(labelfield),
                 "      .title('Create new entry')",
                 '      .buttons( {label}_buttons )'.format(label=labelfield),
                 '      .create();',
                 '  } );',
                 '',
                 '  {}_editor = new $.fn.dataTable.Editor( '.format(labelfield)]
                js += edoptsjson
                js += [
                 '  );',
                 '  // if form closes, reopen previous editor',
                 '  {}_editor'.format(labelfield),
                 '    .on("close", function () {',
                 '      if (!pushing) {',
                 '        popeditor( );',
                 '        curreditor.field( parentname ).set( {}_{}_lastval );'.format(parentfield, valuefield),
                 '      };',
                 '  });',
                 '',
                 '} );']
                response = make_response('\n'.join(js))
                response.headers.set('Content-Type', 'application/javascript')
                return response
            return super(DbCrudApi, self).get()

    def saformurl(self, **kwargs):
        """
        standalone form url
        """
        args = urlencode(kwargs)
        url = '{}/saformjs?{}'.format(url_for('.' + self.my_view.__name__), args)
        return url

    def register(self):
        name = self.endpoint.split('.')[(-1)]
        super(DbCrudApi, self).register()
        self.app.add_url_rule(('{}/saformjs'.format(self.rule)), view_func=(self.my_view), methods=['GET'])
        self.app.add_url_rule(('{}/saform'.format(self.rule)), view_func=(self.my_view), methods=['GET'])

    def open(self):
        """
        retrieve all the data in the indicated table
        """
        if debug:
            current_app.logger.debug('DbCrudApi.open()')
        if debug:
            current_app.logger.debug('DbCrudApi.open: self.db = {}, self.model = {}'.format(self.db, self.model))
        if not self.serverside:
            query = (self.model.query.filter_by)(**self.queryparams)
            self.rows = iter(query.all())
        else:
            query = (self.db.session.query().select_from(self.model).filter_by)(**self.queryparams)
            args = request.args.to_dict()
            rowTable = DataTables(args, query, self.servercolumns)
            output = rowTable.output_result()
            if 'error' in output:
                raise ParameterError(output['error'])
            self.output_result = output

    def nexttablerow(self):
        """
        since open has done all the work, tell the caller we're done
        """
        if debug:
            current_app.logger.debug('DbCrudApi.nexttablerow()')
        if not self.serverside:
            dbrecord = next(self.rows)
            return self.dte.get_response_data(dbrecord)
        raise StopIteration

    def close(self):
        if debug:
            current_app.logger.debug('DbCrudApi.close()')

    def validatedb(self, action, formdata):
        if debug:
            current_app.logger.debug('DbCrudApi.validatedb({})'.format(action))
        if action == 'refresh':
            return []
        else:
            results = self.callervalidate(action, formdata)
            if self.checkrequired:
                for col in self.clientcolumns:
                    field = col['data']
                    if 'className' in col:
                        if 'field_req' in col['className'].split(' '):
                            if not isinstance(formdata[field], str) and 'id' in formdata[field]:
                                if not formdata[field]['id']:
                                    results.append({'name':'{}.id'.format(field),  'status':'please select'})
                        if not formdata[field]:
                            results.append({'name':field,  'status':'please supply'})

            if action == 'create' and self.uniquecols:
                dbrow = self.model()
                self.dte.set_dbrow(formdata, dbrow)
                for field in self.uniquecols:
                    rows = ((self.model.query.filter_by)(**self.queryparams).filter_by)(**{field: getattr(dbrow, field)}).all()
                    if len(rows) == 1 and rows[0].id != dbrow.id or len(rows) >= 2:
                        results.append({'name':field,  'status':'duplicate found, must be unique'})

                self.db.session.rollback()
            return results

    def createrow(self, formdata):
        """
        creates row in database

        :param formdata: data from create form
        :rtype: returned row for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        dbrow = self.model()
        if debug:
            current_app.logger.debug('createrow(): self.dbmapping = {}'.format(self.dbmapping))
        self.dte.set_dbrow(formdata, dbrow)
        if debug:
            current_app.logger.debug('createrow(): creating dbrow={}'.format(dbrow.__dict__))
        self.db.session.add(dbrow)
        if debug:
            current_app.logger.debug('createrow(): created dbrow={}'.format(dbrow.__dict__))
        self.db.session.flush()
        if debug:
            current_app.logger.debug('createrow(): flushed dbrow={}'.format(dbrow.__dict__))
        self.created_id = dbrow.id
        thisrow = self.dte.get_response_data(dbrow)
        return thisrow

    def updaterow(self, thisid, formdata):
        """
        updates row in database

        :param thisid: id of row to be updated
        :param formdata: data from create form
        :rtype: returned row for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        if debug:
            current_app.logger.debug('updaterow({},{})'.format(thisid, formdata))
        lock = RLock()
        with lock:
            queryparams = {'id': thisid}
            if self.version_id_col:
                queryparams[self.version_id_col] = formdata[self.version_id_col]
            dbrow = (self.model.query.filter_by)(**queryparams).one_or_none()
            if dbrow:
                if debug:
                    current_app.logger.debug('editing id={} dbrow={}'.format(thisid, dbrow.__dict__))
                self.dte.set_dbrow(formdata, dbrow)
                if debug:
                    current_app.logger.debug('after edit id={} dbrow={}'.format(thisid, dbrow.__dict__))
                thisrow = self.dte.get_response_data(dbrow)
                return thisrow
            self._error = 'Someone updated this record while your edit form was open -- close the form and try your edit again'
            raise staleData

    def deleterow(self, thisid):
        """
        deletes row in database

        :param thisid: id of row to be updated
        :rtype: returned row for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        dbrow = self.model.query.filter_by(id=thisid).one()
        if debug:
            current_app.logger.debug('deleting id={} dbrow={}'.format(thisid, dbrow.__dict__))
        self.db.session.delete(dbrow)
        return []

    def refreshrows(self, ids):
        """
        refresh row(s) from database

        :param ids: comma separated ids of row to be refreshed
        :rtype: list of returned rows for rendering, e.g., from DataTablesEditor.get_response_data()
        """
        theseids = ids.split(',')
        responsedata = []
        for thisid in theseids:
            dbrow = self.model.query.filter_by(id=thisid).one()
            responsedata.append(self.dte.get_response_data(dbrow))

        return responsedata

    def commit(self):
        self.db.session.commit()

    def rollback(self):
        self.db.session.rollback()


class DbCrudApiRolePermissions(DbCrudApi):
    __doc__ = "\n    This class extends DbCrudApi which, in turn, extends CrudApi. This extension uses flask_security\n    to do role checking for the current user.\n\n    Caller should use roles_accepted OR roles_required but not both.\n\n    Additional parameters for this class:\n\n        roles_accepted: None, 'role', ['role1', 'role2', ...] - user must have at least one of the specified roles\n        roles_required: None, 'role', ['role1', 'role2', ...] - user must have all of the specified roles\n    "
    from flask_security import current_user

    def __init__(self, **kwargs):
        if debug:
            current_app.logger.debug('DbCrudApiRolePermissions.__init__()')
        else:
            args = dict(roles_accepted=None, roles_required=None)
            args.update(kwargs)
            (super(DbCrudApiRolePermissions, self).__init__)(**args)
            if self.roles_accepted:
                if self.roles_required:
                    raise ParameterError('use roles_accepted OR roles_required but not both')
            if self.roles_accepted:
                if not isinstance(self.roles_accepted, list):
                    self.roles_accepted = [
                     self.roles_accepted]
            if self.roles_required:
                if not isinstance(self.roles_required, list):
                    self.roles_required = [
                     self.roles_required]

    def permission(self):
        """
        determine if current user is permitted to use the view
        """
        if debug:
            current_app.logger.debug('DbCrudApiRolePermissions.permission()')
        elif debug:
            current_app.logger.debug('permission: roles_accepted = {} roles_required = {}'.format(self.roles_accepted, self.roles_required))
        else:
            if not self.roles_accepted:
                if not self.roles_required:
                    allowed = True
            if self.roles_accepted:
                allowed = False
                for role in self.roles_accepted:
                    if self.current_user.has_role(role):
                        allowed = True
                        break

            elif self.roles_required:
                allowed = True
                for role in self.roles_required:
                    if not self.current_user.has_role(role):
                        allowed = False
                        break

        return allowed


class CrudFiles(MethodView):
    __doc__ = '\n    provides files support for CrudApi\n\n    usage:\n        filesinst = CrudFiles([arguments]):\n        apiinst - CrudApi(files=filesinst, [other arguments])\n        apiinst.register()\n    '

    def __init__(self, **kwargs):
        if debug:
            print('CrudFiles.__init__() **kwargs={}'.format(kwargs))
        self.kwargs = kwargs
        args = dict(app=None, uploadendpoint=None,
          uploadrule=None,
          endpointvalues={})
        args.update(kwargs)
        for key in args:
            setattr(self, key, args[key])

        self.uploadrule = self.uploadrule or '/' + self.uploadendpoint
        self.credentials = None

    def register(self):
        name = self.uploadendpoint.split('.')[(-1)]
        if debug:
            print('CrudFiles.register()')
        upload_view = (self.as_view)(name, **self.kwargs)
        self.app.add_url_rule(('{}'.format)((self.uploadrule), **self.endpointvalues), view_func=upload_view, methods=['POST'])

    @_uploadmethod()
    def post(self):
        self._responsedata = self.upload()

    def list(self):
        """
        must be overridden

        return list of files

        return value must be set to the following, as defined in https://editor.datatables.net/manual/server#File-upload

             {
                table1 : {
                            fileid1 : metadata1,
                            fileid2 : metadata2,
                            ...
                         },
                table2 : {
                            etc.
                         }
             }

        where:
            tablename is name for table which will be stored in DataTables and Editor
            fileid is scalar file identifier, e.g., database id
            metadata is dict describing file, e.g., 
                'filename' : filename
                'web_path' : path to file, etc

        
        :rtype: return value as described above
        """
        pass

    def upload(self):
        """
        must override, but this must be called

        receive an uploaded file

        returnvalue dict must include at least 
        the following keys, as defined in 
        https://editor.datatables.net/manual/server#File-upload

            {
             'upload' : {'id': fileid },
             'files'  : {
                        table : {
                            fileid : metadata
                        },
             optkey1  : optdata1
            ...
            }

        where:
            fileid is scalar file identifier, e.g., database id
            tablename is name for table which will be stored in DataTables and Editor
            metadata is dict describing file, e.g., 
                'filename' : filename
                'web_path' : path to file, etc
            optkeyn is optional key

        if optional keys are provided will be sent along with the data 

        :rtype: return value as described above
        """
        pass


def deepupdate(obj, val, newval):
    """
    recursively searches obj object and replaces any val values with newval
    does not update opj
    returns resultant object
    
    :param obj: object which requires updating
    :param val: val to look for
    :param newval: replacement for val
    """
    thisobj = deepcopy(obj)
    if isinstance(thisobj, dict):
        for k in thisobj:
            thisobj[k] = deepupdate(thisobj[k], val, newval)

    else:
        if isinstance(thisobj, list):
            for k in range(len(thisobj)):
                thisobj[k] = deepupdate(thisobj[k], val, newval)

        else:
            if thisobj == val:
                thisobj = newval
    return thisobj