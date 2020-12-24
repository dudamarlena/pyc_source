# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tgext/subform/controller.py
# Compiled at: 2013-01-29 22:57:48
import inspect
from formencode import Invalid
from tg import expose
from tgext.crud.controller import errors, CrudRestController
from tgext.crud.decorators import catch_errors, registered_validate
from sprox.formbase import AddRecordForm, EditableForm

class SubformMixin(object):

    @property
    def _model(self):
        model = self.model
        if inspect.isfunction(model):
            model = model()
        return model

    def _get_subtype(self, name):
        model = self._model
        field = self.new_form.__provider__.get_field(model, name)
        if hasattr(field, 'argument'):
            model = field.argument
        else:
            if inspect.isfunction(target_field):
                model = target_field()
            if inspect.isfunction(model):
                return model()
        return model

    @catch_errors(errors)
    @expose('json')
    def subtype_post(self, *args, **kw):
        model = self._model
        if '__subtype' in kw:
            model = self._get_subtype(kw['__subtype'])
            del kw['__subtype']
        provider = self.new_form.__provider__
        obj = provider.create(model, params=kw)
        provider.session.flush()
        return provider.dictify(obj)

    @expose('json')
    def validate(self, *args, **kw):
        subtype = kw['__subtype']
        method = kw.get('__method', 'add')
        form = self.new_form
        if method == 'edit':
            form = self.edit_form
        widget = form.__widget__.children[subtype]
        try:
            widget.__subform__.validate(kw)
        except Invalid as e:
            return e.unpack_errors()

        return {}


class SubformController(CrudRestController, SubformMixin):
    pass