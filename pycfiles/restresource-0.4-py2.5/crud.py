# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/restresource/crud.py
# Compiled at: 2008-09-17 13:56:21
import cherrypy
from turbogears import expose, redirect
from turbogears import validate, validators, error_handler
from turbogears.widgets import *
import sqlobject

def error_response(o):
    """if o is a string then it's an error response
    utility function to return errors from a sub-call to validate/error_handler
    decorated function 
    """
    if not isinstance(o, str):
        return False
    return o


def _soc_default_SOUnicodeCol(f):
    return {f: TextField(name=f)}


def _soc_default_SODateCol(f):
    return {f: CalendarDatePicker(name=f, validator=validators.DateConverter())}


def _soc_default_SODateTimeCol(f):
    return {f: CalendarDateTimePicker(name=f, validator=validators.DateTimeConverter())}


def _soc_default_SOForeignKey(f):
    return {}


def _soc_default_SOBoolCol(f):
    return {f: CheckBox(name=f)}


def _soc_default_SOIntCol(f):
    return {f: TextField(name=f, validator=validators.Int())}


def _soc_default_Number(f):
    return {f: TextField(name=f, validator=validators.Number())}


_soc_table_so_mapper = dict([
 (
  sqlobject.col.SOUnicodeCol, _soc_default_SOUnicodeCol),
 (
  sqlobject.col.SOStringCol, _soc_default_SOUnicodeCol),
 (
  sqlobject.col.SODateTimeCol, _soc_default_SODateTimeCol),
 (
  sqlobject.col.SODateCol, _soc_default_SODateCol),
 (
  sqlobject.col.SOForeignKey, _soc_default_SOForeignKey),
 (
  sqlobject.col.SOBoolCol, _soc_default_SOBoolCol),
 (
  sqlobject.col.SOIntCol, _soc_default_SOIntCol),
 (
  sqlobject.col.SODecimalCol, _soc_default_Number),
 (
  sqlobject.col.SOCurrencyCol, _soc_default_Number),
 (
  sqlobject.col.SOFloatCol, _soc_default_Number),
 (
  sqlobject.col.SOEnumCol, _soc_default_SOUnicodeCol)])

class SOController:
    """

    """
    soClass = None
    validate_create_form = lambda self: self.getform('create')
    validate_update_form = lambda self: self.getform('update')

    def __init__(self, soClass):
        self.soClass = soClass

    def record_dict(self, soObj, **kw):
        soDict = dict()
        for (f, v) in self.columns().items():
            soDict[f] = getattr(soObj, f, None)
            if type(v) == sqlobject.col.SOForeignKey:
                field_sansID = f[:-2]
                field_val = getattr(soObj, field_sansID, None)
                if field_val is not None:
                    soDict[field_sansID] = self.record_dict(field_val)
                else:
                    soDict[field_sansID] = None

        soDict['id'] = soObj.id
        for k in kw:
            soDict[k] = kw[k]

        return soDict

    def columns(self):
        columns = {}
        for x in self.soClass.__mro__:
            y = x.sqlmeta.columns.items()
            if len(y) == 0:
                break
            columns.update(y)

        if 'childName' in columns:
            del columns['childName']
        return columns

    def name(self):
        return self.soClass.__name__

    @staticmethod
    def parentValues(self):
        """return SQLObject dict of """
        kw = dict()
        parentDict = dict([ (p.sqlmeta.table, p.id) for p in self.parents ])
        for (c, t) in self.crud.columns().items():
            if type(t) == sqlobject.col.SOForeignKey and t.foreignKey.lower() in parentDict:
                kw[c] = parentDict[t.foreignKey.lower()]

        return kw

    def field_widgets(self):
        """return a dictionary of fields from self.soClass to build the FormFields
        Widget object.
        """
        field_dict = dict()
        for (f, fclass) in self.columns().items():
            field_dict.update(_soc_table_so_mapper[type(fclass)](f))

        return field_dict

    @staticmethod
    def edit_form(self, table, tg_errors=None, tg_flash=None, **kwargs):
        kwargs.update(record=table, columns=self.crud.columns().keys(), record_dict=self.crud.record_dict(table), form=self.getform('update'), tg_errors=tg_errors, tg_flash=tg_flash)
        return kwargs

    @staticmethod
    def add_form(self, tg_errors=None, tg_flash=None, **kwargs):
        kwargs.update(form=self.getform('create'), columns=self.crud.columns().keys(), tg_errors=tg_errors, tg_flash=tg_flash)
        return kwargs

    def update_error(self, *pargs, **kwargs):
        cherrypy.response.status = 400
        return self.get_edit_form(*pargs, **kwargs)

    def create_error(self, *pargs, **kwargs):
        cherrypy.response.status = 400
        return self.get_add_form(**kwargs)

    @staticmethod
    @validate(form=validate_create_form)
    @error_handler(create_error)
    def create_validation(self, **kw):
        return kw

    @staticmethod
    @validate(form=validate_update_form)
    @error_handler(update_error)
    def update_validation(self, table, **kw):
        return kw

    @staticmethod
    def create(self, table, **kw):
        if len(self.parents) > 0:
            kw.update(self.crud.parentValues(self))
        if table is None:
            table = self.crud.soClass(**kw)
        else:
            table.set(**kw)
        table._connection.commit()
        return table

    @staticmethod
    def read(self, table, **kw):
        return dict(record=table, columns=self.crud.columns().keys())

    @staticmethod
    def update(self, table, **kw):
        table.set(**kw)
        table._connection.commit()
        return table

    @staticmethod
    def delete(self, table):
        table.destroySelf()
        table._connection.commit()
        return table

    @staticmethod
    def list(self, **kw):
        """what is called for /foo instead of /foo/2 """
        return self.search(**kw)

    @staticmethod
    def search(self, **kw):
        kw.update(self.crud.parentValues(self))
        results = list(self.crud.soClass.selectBy(**kw))
        return dict(members=results, columns=self.crud.columns().keys())


class CrudController:
    """inherited by a CherryPy controller, this depends on a 'crud'
    attribute to do the real work.  This layer should be decorated
    with templates.  The corresponding crud functions should be
    decorated with security/identity/validation/error_handler wrappers.

    When overriding these methods, you will often just copy this version
    to get started.
    """
    FormFields = WidgetsList
    Form = TableForm

    def initfields(self, action, field_dict):
        """can add/delete/modify the fields in fielddict from defaults
           before returning the modified field_dict object
           param @action is 'create' or 'update'
        """
        return field_dict

    def initform(self, action):
        FormFields = type('FormFields', (
         self.FormFields,), self.initfields(action, self.crud.field_widgets()))
        Form = self.Form
        fields = FormFields()
        return Form(name=str(self.crud.name() + '_' + action).lower(), fields=fields)

    def getform(self, action):
        if not hasattr(self, '_form'):
            self._form = dict()
        if action not in self._form:
            self._form[action] = self.initform(action)
        return self._form[action]

    def REST_instantiate(self, id, **kwargs):
        try:
            return self.crud.soClass.get(id)
        except:
            return

        return

    def REST_create(self, **kwargs):
        """Create class here only if there are inherited values
           (e.g. from parent controllers perhaps)"""
        return

    @expose(template='kid:restresource.templates.view', format='xhtml', accept_format='text/html')
    @expose(template='kid:restresource.templates.view', format='xhtml', accept_format='text/xml', content_type='text/xml')
    @expose(template='json', accept_format='text/javascript')
    def read(self, table, **kw):
        return self.crud.read(self, table, **kw)

    read.expose_resource = True

    @expose(template='kid:restresource.templates.edit', format='xhtml', accept_format='text/html')
    @expose(template='kid:restresource.templates.edit', format='xhtml', accept_format='text/xml', content_type='text/xml')
    def get_edit_form(self, table, **kw):
        return self.crud.edit_form(self, table, **kw)

    get_edit_form.expose_resource = True

    @expose(template='kid:restresource.templates.add', format='xhtml', accept_format='text/html')
    @expose(template='kid:restresource.templates.add', format='xhtml', accept_format='text/xml', content_type='text/xml')
    def get_add_form(self, **kw):
        return self.crud.add_form(self, **kw)

    @expose(template='kid:restresource.templates.list')
    @expose(template='json', accept_format='text/javascript')
    def list(self, *p, **kw):
        return self.crud.list(self, *p, **kw)

    @expose(template='kid:restresource.templates.list')
    @expose(template='json', accept_format='text/javascript')
    def search(self, *p, **kw):
        return self.crud.search(self, *p, **kw)

    search.expose_resource = True

    def post(self, **kw):
        """when a POST goes directly to /col/"""
        return self.create(self.REST_create(**kw), **kw)

    post.exposed = True

    def create(self, table, **kw):
        kw = self.crud.create_validation(self, **kw)
        return error_response(kw) or error_response(self.crud.create(self, table, **kw)) or self.create_success(table, **kw)

    create.expose_resource = True

    def update(self, table, **kw):
        kw = self.crud.update_validation(self, table, **kw)
        return error_response(kw) or error_response(self.crud.update(self, table, **kw)) or self.update_success(table, **kw)

    update.expose_resource = True

    def update_success(self, table, **kw):
        return 'ok'

    def create_success(self, table, **kw):
        return 'ok'

    def delete(self, table, **kw):
        return error_response(self.crud.delete(self, table, **kw)) or 'ok'

    delete.expose_resource = True