# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hncforms\handlers.py
# Compiled at: 2013-05-23 13:39:15
from collections import OrderedDict
import formencode
from formencode.validators import Invalid
from formencode.variabledecode import variable_decode
import logging
from paste.httpexceptions import HTTPNotImplemented
from pyramid.httpexceptions import HTTPFound
from hncforms.messages import GenericErrorMessage, GenericSuccessMessage
log = logging.getLogger(__name__)
_ = lambda s: s

class InvalidCSRFToken(Exception):
    pass


class BaseHandler(object):

    def __init__(self, context, request):
        self.request = request
        self.context = context


class ValidatedFormHandlerMetaClass(type):

    def __new__(cls, name, bases, dct):
        if 'schemas' not in dct:
            if 'form' in dct:
                form = dct['form']
                dct['schemas'] = OrderedDict([(form.id, form)])
            elif 'forms' in dct:
                dct['schemas'] = OrderedDict([ (form.id, form) for form in dct['forms'] ])
        return super(ValidatedFormHandlerMetaClass, cls).__new__(cls, name, bases, dct)


class FormHandler(object):
    __metaclass__ = ValidatedFormHandlerMetaClass

    def __init__(self, context=None, request=None):
        self.request = request
        self.context = context
        self.result = {'values': {}, 'errors': {}, 'schemas': self.schemas, 'formencode': formencode}
        self.result['values'].update([ (k, {}) for k in self.schemas.keys() ])
        self.result['errors'].update([ (k, {}) for k in self.schemas.keys() ])

    def pre_fill_values(self, request, result):
        return result

    def add_globals(self, request, result):
        return result

    def GET(self):
        self.request.session.get_csrf_token()
        self.result = self.add_globals(self.request, self.result)
        self.result = self.pre_fill_values(self.request, self.result)
        return self.result

    def POST(self):
        try:
            return self.validate_form()
        except InvalidCSRFToken:
            self.result = self.add_globals(self.request, self.result)
            return self.result

    ajaxGET = GET

    def ajax(self):
        result = self.validate_json()
        return result

    def validate_form(self):
        values = variable_decode(self.request.params)
        schema_id = values.get('type')
        if not schema_id:
            raise HTTPNotImplemented()
        try:
            resp = self.validate_values(values)
        except Invalid as error:
            log.error(error.error_dict)
            self.result['values'][schema_id] = error.value or {}
            self.result['errors'][schema_id] = error.error_dict or {}
            self.request.response.status_int = 401
        else:
            if resp.get('message'):
                if resp.get('success') == True:
                    self.request.session.flash(GenericSuccessMessage(resp.get('message')), 'generic_messages')
                elif resp.get('success') == False:
                    self.request.session.flash(GenericErrorMessage(resp.get('message')), 'generic_messages')
            if resp.get('redirect'):
                self.request.fwd_raw(resp.get('redirect'))
            self.result['values'][schema_id] = resp.get('values', values)
            self.result['errors'][schema_id] = resp.get('errors', {})
            self.request.response.status_int = 401

        self.result = self.add_globals(self.request, self.result)
        return self.result

    def validate_json(self, renderTemplates={}):
        values = self.request.json_body
        schema_id = values['type']

        def wrap_errors(errors):
            map = {}
            map[schema_id] = errors
            return formencode.variabledecode.variable_encode(map)

        try:
            form_result = self.validate_values(values)
        except Invalid as error:
            return {'success': False, 'values': error.value or {}, 'errors': wrap_errors(error.unpack_errors())}
        except HTTPFound as e:
            return {'redirect': e.location}
        except InvalidCSRFToken:
            return {'success': False, 'errorMessage': _('An error occured, please try again.')}

        form_result.setdefault('success', False)
        form_result['errors'] = wrap_errors(form_result.get('errors', {}))
        return form_result

    def validate_values(self, values, renderTemplates={}):
        req = self.request
        if values.get('token') != req.session.get_csrf_token():
            raise InvalidCSRFToken()
        try:
            schema_id = values['type']
            schema = self.schemas[schema_id]
            form = schema.getSchema(req, values)
        except KeyError as e:
            raise HTTPNotImplemented('Unexpected submission type!')
        else:
            form_result = form.to_python(values.get(schema_id), state=self.request)
            return schema.on_success(self.request, form_result)