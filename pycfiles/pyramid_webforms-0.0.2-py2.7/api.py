# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_webforms/api.py
# Compiled at: 2013-01-28 11:17:35
from __future__ import unicode_literals
import re, copy, inspect, six, formencode
from webhelpers.html import literal, tags
from pyramid.renderers import render
from pyramid.httpexceptions import exception_response
from pyramid.mako_templating import MakoRendererFactoryHelper
from pyramid.i18n import get_localizer, TranslationString, TranslationStringFactory
_ = original_gettext = TranslationStringFactory(b'pyramid_webforms')
forms_renderer_factory = MakoRendererFactoryHelper(b'p_wf_mako.')

class FormencodeState(object):
    """"Dummy" state class for formencode"""
    _ = staticmethod(original_gettext)

    def __init__(self, **kwargs):
        for arg in kwargs:
            self.__dict__[arg] = kwargs[arg]


class PrototypeSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True


class CSRFTokenValidator(formencode.validators.UnicodeString):
    not_empty = True
    strip = True

    def validate_python(self, value, state):
        super(CSRFTokenValidator, self).validate_python(value, state)
        request = state.request
        token = request.session.get_csrf_token()
        if token != value:
            localizer = get_localizer(request)
            raise formencode.Invalid(localizer.translate(_(b'Invalid CSRF token.')), value, state)


CSRF_TOKEN_KEY = b'_at'
CSRF_TOKEN_FIELD = {b'type': b'hidden', 
   b'value': b'', 
   b'validator': CSRFTokenValidator}
csrf_detected_message = b'Cross-site request forgery detected, request denied. See http://en.wikipedia.org/wiki/Cross-site_request_forgery for more information.'

def authenticated_form(request):
    submitted_token = request.POST.get(CSRF_TOKEN_KEY)
    token = request.session.get_csrf_token()
    return submitted_token is not None and submitted_token == token


def authenticate_form(func):

    def inner(context, request):
        if not request.POST:
            return func(context, request)
        if authenticated_form(request):
            return func(context, request)
        raise exception_response(403, detail=csrf_detected_message)

    return inner


def _secure_form(action, method=b'POST', multipart=False, **kwargs):
    """Start a form tag that points the action to an url. This
    form tag will also include the hidden field containing
    the auth token.

    The ``action`` option should be given either as a string, or as a
    ``request.route_url()`` function. The method for the form defaults to POST.

    Options:

    ``multipart``
        If set to True, the enctype is set to "multipart/form-data".
    ``method``
        The method to use when submitting the form, usually either
        "GET" or "POST". If "PUT", "DELETE", or another verb is used, a
        hidden input with name _method is added to simulate the verb
        over POST.

    """
    return literal(tags.form(action, method, multipart, **kwargs))


class FieldError(Exception):
    pass


class DeclarativeMeta(type):

    def __new__(mcs, class_name, bases, new_attrs):
        cls = type.__new__(mcs, class_name, bases, new_attrs)
        cls.__classinit__.__func__(cls, new_attrs)
        return cls


FORM_ATTRIBUTES_RE = re.compile(b'_[a-z0-9][a-z0-9_]*[a-z0-9]_', re.IGNORECASE)
ACTION_CALL_SAME_VIEW = b''

class Form(object):
    __metaclass__ = DeclarativeMeta
    _fields = {}
    _hidden = {}
    _params = {b'fieldsets': [], b'filter': [], b'validation_schema': None, 
       b'method': b'post'}
    Invalid = formencode.Invalid

    def __classinit__(self, new_attrs):
        self._fields = copy.copy(self._fields)
        self._hidden = copy.copy(self._hidden)
        self._params = copy.deepcopy(self._params)
        for name, val in new_attrs.items():
            if name.startswith(b'__') or inspect.ismethod(val) or isinstance(val, classmethod) or val is formencode.Invalid:
                continue
            elif FORM_ATTRIBUTES_RE.match(name):
                if name == b'_fieldsets_':
                    self._params[b'fieldsets'] = self._compose_fieldsets(val)
                else:
                    self._params[name[1:-1]] = val
            elif val.get(b'type') == b'hidden':
                self._hidden[name] = val
            else:
                self._fields[name] = val

        for item in self._params[b'filter']:
            try:
                self._fields.pop(item)
            except KeyError:
                self._hidden.pop(item)

            for fieldset in self._params[b'fieldsets']:
                new_fields_list = []
                for idx, field in enumerate(fieldset[b'fields']):
                    if field != item:
                        new_fields_list.append(field)

                fieldset[b'fields'] = new_fields_list

        self._params[b'filter'] = []
        if self._params.get(b'method', b'post') == b'post':
            if CSRF_TOKEN_KEY not in self._hidden:
                self._hidden[CSRF_TOKEN_KEY] = CSRF_TOKEN_FIELD
        elif CSRF_TOKEN_KEY in self._hidden:
            del self._hidden[CSRF_TOKEN_KEY]
        self._params[b'validation_schema'] = self._compose_validator()

    @classmethod
    def _compose_fieldsets(cls, val):
        fieldsets = []
        for fieldset in val:
            data = {}
            for item in fieldset:
                if isinstance(item, TranslationString):
                    data[b'name'] = item
                elif isinstance(item, six.string_types):
                    data[b'optional'] = item == b'optional'
                elif isinstance(item, list):
                    data[b'fields'] = item
                else:
                    continue

            fieldsets.append(data)

        return fieldsets

    @classmethod
    def _compose_validator(cls):
        schema = PrototypeSchema()
        for name in cls._fields:
            validator = cls._fields[name].get(b'validator')
            if validator:
                schema.add_field(name, validator)

        for name in cls._hidden:
            validator = cls._hidden[name].get(b'validator')
            if validator:
                schema.add_field(name, validator)

        chained_validators = cls._params.pop(b'chained_validators', [])
        for validator in chained_validators:
            schema.add_chained_validator(validator)

        return schema

    @classmethod
    def validate(cls, request, state=None):
        if cls._params[b'method'] == b'post':
            data = request.POST
        elif cls._params[b'method'] == b'get':
            data = request.GET
        else:
            data = request.params
        if state is None:
            state = FormencodeState(request=request)
        data = cls._params[b'validation_schema'].to_python(data, state)
        return data

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data
        self._cached_parts = {}
        return

    def __call__(self, request, part=b'all'):
        localizer = get_localizer(request)
        if self._params.get(b'method', b'post') == b'post':
            self.data[CSRF_TOKEN_KEY] = {b'value': request.session.get_csrf_token()}
        if self._cached_parts.get(b'buttons') is None:
            alternate_url = self._params.get(b'alternate_url', b'')
            if alternate_url:
                if isinstance(alternate_url, dict):
                    url_kw = copy.copy(alternate_url)
                    name = url_kw.pop(b'name', None)
                    alternate_url = request.route_path(name, **url_kw)
                template_path = request.registry.settings.get(b'pyramid_webforms.submit_alternate_tpl', b'pyramid_webforms:templates/submit_alternate.p_wf_mako')
                submit_btn = render(template_path, {b'form_submit_text': self._params.get(b'submit_text', localizer.translate(_(b'Submit'))), 
                   b'form_or_text': self._params.get(b'or_text', localizer.translate(_(b'or'))), 
                   b'form_alternate_url': alternate_url, 
                   b'form_alternate_text': self._params.get(b'alternate_text', b'')}, request)
            else:
                template_path = request.registry.settings.get(b'pyramid_webforms.submit_tpl', b'pyramid_webforms:templates/submit.p_wf_mako')
                submit_btn = render(template_path, {b'form_submit_text': self._params.get(b'submit_text', localizer.translate(_(b'Submit')))}, request)
            self._cached_parts[b'buttons'] = literal(submit_btn)
        if self._cached_parts.get(b'fields') is None:
            output = []
            for fields in self._params[b'fieldsets']:
                output.append(self._generate_fields(request, fields, self.data))

            self._cached_parts[b'fields'] = literal((b'').join(output))
        if self._cached_parts.get(b'attributes') is None:
            action = self.data.get(b'_action_')
            if action is None:
                action_params = self._params.get(b'action', {})
                if action_params:
                    url_kw = copy.copy(action_params)
                    name = url_kw.pop(b'name', None)
                    action = request.route_path(name, **url_kw)
                else:
                    action = ACTION_CALL_SAME_VIEW
            hidden_fields = []
            for name, data in self._hidden.items():
                value = self.data.get(name, {}).get(b'value', data.get(b'value'))
                hidden_fields.append(tags.__dict__[b'hidden'](name, value))

            self._cached_parts[b'attributes'] = literal((b'{}{}').format(_secure_form(action, id=self._params.get(b'id'), class_=self._params.get(b'class'), method=self._params.get(b'method', b'post'), multipart=self._params.get(b'multipart'), target=self._params.get(b'target'), style=self._params.get(b'style'), **self._params.get(b'html5_attrs', {})), (b'').join(hidden_fields)))
        if self._cached_parts.get(b'footer') is None:
            self._cached_parts[b'footer'] = literal(b'</form>')
        if part == b'attributes':
            return self._cached_parts[b'attributes']
        else:
            if part == b'fields':
                return self._cached_parts[b'fields']
            else:
                if part == b'buttons':
                    return self._cached_parts[b'buttons']
                if part == b'footer':
                    return self._cached_parts[b'footer']
                template_path = request.registry.settings.get(b'pyramid_webforms.form_tpl', b'pyramid_webforms:templates/form.p_wf_mako')
                return literal(render(template_path, {b'form_attributes': self._cached_parts[b'attributes'], 
                   b'form_fields': self._cached_parts[b'fields'], 
                   b'form_buttons': self._cached_parts[b'buttons'], 
                   b'form_footer': self._cached_parts[b'footer']}, request))

            return

    @classmethod
    def _generate_fields(self, request, fields_list, override_data):
        html = []
        for name in fields_list[b'fields']:
            field = self._fields[name]
            values = {b'with_tip': self._params.get(b'with_tip', True)}
            values.update(field)
            data = override_data.get(name, {})
            values.update(data)
            values.pop(b'validator', None)
            input = InputField(name=name, **values)
            html.append(input(request))

        if not html:
            return b''
        else:
            title = fields_list.get(b'name', b'')
            template_path = request.registry.settings.get(b'pyramid_webforms.fieldset_tpl', b'pyramid_webforms:templates/fieldset.p_wf_mako')
            return literal(render(template_path, {b'fieldset_title': title, 
               b'fieldset_fields': literal((b'').join(html))}, request))


class InputField(object):
    tag_types = {b'date': b'text'}

    def __init__(self, type=b'html', name=b'', value=None, selected=False, title=b'', tip=b'', **kw):
        if type != b'html':
            try:
                assert type in tags.__dict__
            except AssertionError:
                if type not in self.tag_types:
                    raise FieldError((b'HTML field type "{}" is not supported by webhelpers package').format(type))

        self.type = type
        self.tag_type = self.tag_types.get(type, type)
        self.name = name
        self.value = value
        self.selected = selected
        self.title = title
        self.tip = tip
        self.kw = kw

    def _prepare_date(self):
        return self._prepare_text()

    def _prepare_textarea(self):
        kwargs = {b'name': self.name, 
           b'id': self.kw.get(b'id'), 
           b'class_': self.kw.get(b'class', b''), 
           b'content': self.value, 
           b'cols': self.kw.get(b'cols', 30), 
           b'rows': self.kw.get(b'rows', 7), 
           b'wrap': self.kw.get(b'wrap', b'SOFT'), 
           b'required': self.kw.get(b'required', None)}
        return kwargs

    def _prepare_select(self):
        return {b'name': self.name, 
           b'id': self.kw.get(b'id'), 
           b'class_': self.kw.get(b'class', b''), 
           b'selected_values': self.value, 
           b'options': self.kw.get(b'options'), 
           b'multiple': self.kw.get(b'multiple', False)}

    def _prepare_text(self):
        return {b'name': self.name, 
           b'type': self.type, 
           b'id': self.kw.get(b'id'), 
           b'class_': self.kw.get(b'class', b''), 
           b'value': self.value, 
           b'size': self.kw.get(b'size'), 
           b'maxlength': self.kw.get(b'maxlength'), 
           b'required': self.kw.get(b'required', None)}

    def _prepare_password(self):
        kwargs = self._prepare_text()
        kwargs[b'type'] = b'password'
        return kwargs

    def _prepare_checkbox(self):
        if self.value is None:
            value = 1
        else:
            value = self.value
        return {b'name': self.name, b'id': self.kw.get(b'id'), 
           b'class_': self.kw.get(b'class', b''), 
           b'value': value, 
           b'checked': self.selected}

    def _prepare_file(self):
        return {b'name': self.name, 
           b'id': self.kw.get(b'id'), 
           b'class_': self.kw.get(b'class', b''), 
           b'multiple': self.kw.get(b'multiple') and b'multiple'}

    def __call__(self, request, name=None, value=None, selected=None, title=None, tip=None, data=None, **kwargs):
        kw = {}
        if data is None:
            data = {}
        if title is None:
            title = self.title
        if tip is None:
            tip = self.tip
        if self.type == b'html':
            input = value or self.value
        else:
            kw.update(self.kw)
            kw.update(**data)
            if name is None:
                name = self.name
            kwargs = self.__getattribute__((b'_prepare_{}').format(self.type))()
            with_tip = self.kw.get(b'with_tip', kwargs.get(b'with_tip', True))
            kwargs[b'class_'] = (b'{var}{const}').format(var=kwargs.get(b'class_', self.type), const=with_tip and b' with-tip' or b'')
            kwargs.update(self.kw.get(b'html5_attrs', {}))
            input = tags.__dict__[self.tag_type](**kwargs)
        extra_html = literal(kw.pop(b'extra_html', b''))
        tip_escape = kw.pop(b'tip_escape', False)
        input_only = kw.pop(b'input_only', False)
        if input_only:
            return input
        else:
            error = request.tmpl_context.form_errors.get(name, b'')
            if error:
                error = field_error(request, error)
            template_path = request.registry.settings.get(b'pyramid_webforms.field_tpl', b'pyramid_webforms:templates/field.p_wf_mako')
            return literal(render(template_path, {b'field_name': name, 
               b'field_title': title, 
               b'field_error_message': error, 
               b'field_input': input, 
               b'field_tip': self.tooltip(request, tip, tip_escape), 
               b'field_extras': extra_html}, request))

    def tooltip(self, request, tip=b'', escape_html=True):
        """Render a tip for current field"""
        if not tip:
            return b''
        if not escape_html:
            tip = literal(tip)
        template_path = request.registry.settings.get(b'pyramid_webforms.tooltip_tpl', b'pyramid_webforms:templates/tooltip.p_wf_mako')
        return literal(render(template_path, {b'tooltip_tip': tip}, request))


def form_errors(request):
    if request.tmpl_context.form_errors:
        template_path = request.registry.settings.get(b'pyramid_webforms.form_error_tpl', b'pyramid_webforms:templates/form_error.p_wf_mako')
        localizer = get_localizer(request)
        return literal(render(template_path, {b'form_error_message': localizer.translate(_(b'Please correct your input parameters.'))}, request))
    return b''


def field_error(request, error):
    template_path = request.registry.settings.get(b'pyramid_webforms.field_error_tpl', b'pyramid_webforms:templates/field_error.p_wf_mako')
    localizer = get_localizer(request)
    return literal(render(template_path, {b'field_error_label': localizer.translate(_(b'Error')), b'field_error_text': error}, request))