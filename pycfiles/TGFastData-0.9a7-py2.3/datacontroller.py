# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgfastdata\datacontroller.py
# Compiled at: 2007-07-14 11:29:06
import re
from turbogears import widgets, database, validators
import turbogears, formmaker
from datawidgets import FastDataGrid, EditForm
import cherrypy, simplejson, formencode
from sqlobject import SQLObjectNotFound, IN
from sqlobject.sresults import SelectResults
from sqlobject.sqlbuilder import SQLExpression

def join_items(sobj):
    d = {}
    for join in database.so_joins(sobj):
        attr_name = join.joinMethodName
        d[attr_name] = list(getattr(sobj, attr_name))

    return d


_mangle_rx = re.compile('_.')

def col2attrname(name):
    if name.endswith('_id'):
        name = name[:-3]
    return _mangle_rx.sub(lambda x: x.group(0)[1].upper(), name)


class BaseDataController(object):
    __module__ = __name__
    sql_class = None
    getter = None

    def __init__(self, sql_class=None, id_column=None, list_filter=None):
        if not (self.sql_class or sql_class):
            raise ValueError('You must set an sql_class to use a DataController')
        if sql_class:
            self.sql_class = sql_class
        if id_column:
            getterName = sql_class.sqlmeta.columns[id_column].alternateMethodName
            self.getter = getattr(self.sql_class, getterName)
        else:
            self.getter = self.sql_class.get
        self._list_filter = list_filter

    def _get_item(self, atom):
        """
        Hook to allow retrieval by something other than meaningless (lame)
        integer primary key.
        """
        try:
            return self.getter(int(atom))
        except SQLObjectNotFound:
            return None

        return

    def default(self, *vpath, **params):
        """Do RESTful-style access to database objects. Based on
        the RESTful resource recipe by Robert Brewer."""
        if not vpath:
            return self.index(**params)
        vpath = list(vpath)
        atom = vpath.pop(0)
        method = getattr(self, atom, None)
        if method and getattr(method, 'expose_container'):
            return method(*vpath, **params)
        item = self._get_item(atom)
        if item is None:
            raise cherrypy.NotFound
        if vpath:
            method = getattr(self, vpath[0], None)
            if method and getattr(method, 'exposed'):
                return method(item, *vpath[1:], **params)
        return self.show(item, *vpath, **params)
        return

    default = turbogears.expose()(default)

    def _filterJoins(self, obj, data):
        jdata = []
        for join in database.so_joins(self.sql_class):
            jname = join.joinMethodName
            if jname in data.keys():
                jdata.append((join, data.pop(jname)))

        return (
         data, jdata)

    def _updateJoins(self, obj, jdata):
        obj_id = getattr(obj, obj.sqlmeta.idName)
        for (join, data) in jdata:
            jname = join.joinMethodName
            addRelation = 'add' + join.addRemoveName
            removeRelation = 'remove' + join.addRemoveName
            if join.hasIntermediateTable():
                relations = getattr(obj, jname)
                for relation in relations:
                    getattr(obj, removeRelation)(relation)

                if data:
                    relations = join.otherClass.select(IN(join.otherClass.q.id, data))
                    for relation in relations:
                        getattr(obj, addRelation)(relation)

            else:
                oldrelations = set(getattr(obj, jname))
                newrelations = []
                join_attr = col2attrname(join.joinColumn)
                for item in data:
                    try:
                        newrelation = join.otherClass.get(item)
                    except SQLObjectNotFound:
                        raise ValueError, 'Invalid ID for related object.'
                    else:
                        if newrelation not in oldrelations:
                            setattr(newrelation, join_attr, obj)
                        newrelations.append(newrelation)

                for relation in oldrelations.difference(newrelations):
                    setattr(relation, join_attr, None)

        return

    def _update(self, obj=None, **data):
        (data, join_data) = self._filterJoins(self.sql_class, data)
        if obj:
            obj.set(**data)
        else:
            obj = self.sql_class(**data)
        self._updateJoins(obj, join_data)
        return obj

    def _get_instances(self):
        if self._list_filter:
            lfilter = self._list_filter
            if isinstance(lfilter, SelectResults):
                return lfilter
            if callable(lfilter):
                lfilter = lfilter()
            if isinstance(lfilter, (SQLExpression, basestring)):
                lfilter = self.sql_class.select(lfilter)
            return lfilter
        else:
            return self.sql_class.select()


class AjaxDataController(BaseDataController):
    """
    A DataController specifically for use with Ajax requests.
    """
    __module__ = __name__

    def __init__(self, sql_class=None, id_column=None, schema=None):
        super(AjaxDataController, self).__init__(sql_class, id_column)
        self.schema = schema

    def _read_incoming_data():
        """
        Returns a tuple containing the incoming data and any errors
        """
        values = simple_json.load(cherrypy.request.body)
        if self.schema:
            try:
                values = self.schema.to_python(values)
            except validators.Invalid, e:
                errors = {}
                for (key, error) in e.error_dict.items():
                    errors[key] = dict(message=str(error), invalid_value=e.value)

                cherrypy.response.status = 400
                return (None, errors)

        return (
         values, None)
        return

    def index(self):
        return dict(objects=self._get_instances(), errors=None)
        return

    index = turbogears.expose(format='json')(index)

    def create(self, **data):
        (obj_data, errors) = self._read_incoming_data()
        if errors:
            cherrypy.response.status = 400
            return dict(id=None, errors=errors)
        obj = self.sql_class(obj_data)
        return dict(id=obj.id, errors=None)
        return

    create = turbogears.expose(format='json')(create)

    def update(self, obj, **data):
        (obj_data, errors) = self._read_incoming_data()
        if errors:
            cherrypy.response.status = 400
            return dict(id=obj.id, errors=errors)
        if 'id' in obj_data:
            if obj_data['id'] != obj.id:
                cherrypy.response.status = 409
                return dict(id=obj.id, errors=dict(id=dict(message='Object ID invalid', value=obj_data['id'])))
            del obj_data['id']
        errors = dict()
        for key in obj_data.keys():
            try:
                col = obj.sqlmeta.columns[key]
                validator = col.validator
                values[key] = validator.to_python(obj_data[key], None)
            except formencode.Invalid, e:
                errors[key] = dict(message=str(e), invalid_value=e.value)
            except KeyError:
                del obj_data[key]

        if errors:
            cherrypy.response.status = 400
            return dict(id=obj.id, errors=errors)
        obj.set(obj_data)
        return dict(id=obj.id, errors=None)
        return

    update = turbogears.expose(format='json')(update)

    def delete(self, obj):
        obj.destroySelf()
        return dict(id=obj.id, errors=None)
        return

    delete = turbogears.expose(format='json')(delete)

    def show(self, obj):
        return dict(object=obj, errors=None)
        return

    show = turbogears.expose(format='json')(show)


class DataController(BaseDataController):
    """Provides basic add/edit/delete capability"""
    __module__ = __name__
    list_widget = FastDataGrid()
    form_widget_class = EditForm
    form_template = 'tgfastdata.templates.form'
    list_template = 'tgfastdata.templates.list'
    item_template = 'tgfastdata.templates.item'
    form_fields = None
    list_fields = None
    object_name = 'Record'

    def __init__(self, sql_class=None, form_widget_class=None, id_column=None, list_widget=None, form_widget=None, object_name=None, form_template=None, list_template=None, item_template=None, form_fields=None, list_fields=None, list_filter=None):
        super(DataController, self).__init__(sql_class, id_column, list_filter)
        if list_fields:
            self.list_fields = list_fields
        if form_fields:
            self.form_fields = form_fields
        if form_widget_class:
            self.form_widget_class = form_widget_class
        if form_widget:
            self.form_widget = form_widget
            self.form_widget_class = form_widget.__class__
        else:
            self.form_widget = self.form_widget_class(fields=formmaker.fields_for(self.sql_class, self.form_fields))
        if object_name:
            self.object_name = object_name
        if list_widget:
            self.list_widget = list_widget
        elif self.list_fields:
            self.list_widget = FastDataGrid(self.list_fields or self.form_fields)
        if form_template:
            self.form_template = form_template
        if list_template:
            self.list_template = list_template
        if item_template:
            self.item_template = item_template

    def _get_form(self):
        return self.form_widget

    def index(self):
        return dict(tg_template=self.list_template, list_widget=self.list_widget, data=self._get_instances())

    index = turbogears.expose()(index)

    def add(self):
        return dict(tg_template=self.form_template, obj=None, form=self.form_widget, action='create')
        return

    add = turbogears.expose()(add)
    add.expose_container = True

    def create(self, **data):
        self._update(**data)
        turbogears.flash('%s Added!' % self.object_name)
        turbogears.redirect('./')

    create = turbogears.expose()(create)
    create = turbogears.validate(form=_get_form)(create)
    create = turbogears.error_handler(add)(create)

    def edit(self, obj):
        values = database.so_to_dict(obj)
        values.update(join_items(obj))
        return dict(tg_template=self.form_template, form=self.form_widget, obj=values, action='update')

    edit = turbogears.expose()(edit)

    def update(self, obj, **data):
        self._update(obj, **data)
        turbogears.flash('Changes Saved!')
        turbogears.redirect('../')

    update = turbogears.expose()(update)
    update = turbogears.validate(form=_get_form)(update)
    update = turbogears.error_handler(edit)(update)

    def delete(self, obj):
        obj.destroySelf()
        turbogears.flash('%s deleted!' % self.object_name)
        turbogears.redirect('../')

    delete = turbogears.expose()(delete)

    def show(self, obj):
        value = database.so_to_dict(obj)
        columns = obj.sqlmeta.columns
        if self.form_fields:
            column_keys = self.form_fields
        else:
            column_keys = columns.keys()
        column_list = [ (formmaker.column_parms(columns[key])['label'], key) for key in column_keys ]
        value['tg_columns'] = column_list
        value['tg_template'] = self.item_template
        return value

    show = turbogears.expose()(show)