# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/forms.py
# Compiled at: 2006-12-26 17:17:52
__doc__ = '\n    pocoo.utils.forms\n    ~~~~~~~~~~~~~~~~~\n\n    Pocoo form validation helpers.\n\n\n    Form Validation\n    ===============\n\n    Validating forms sucks. To simplify it, Pocoo provides some classes\n    for form validation.\n\n\n    Application Side\n    ----------------\n\n    Here an example form used in `pocoo.pkg.core.forms`::\n\n        from pocoo.utils import forms\n        from pocoo.utils.validators import isEmail, isSameValue\n        from pocoo.pkg.core.validators import isAvailableUsername,              isStrongPassword\n\n        def get_password_error(form, field):\n            _ = form.req.gettext\n            return _(\'The two passwords don\'t match.\')\n\n        class RegisterForm(forms.Form):\n            username = forms.TextField(isAvailableUsername())\n            email = forms.TextField(isEmail())\n            password = forms.PasswordField(isStrongPassword())\n            password2 = forms.PasswordField(isSameValue(\'password\',\n                                            get_password_error))\n\n    As you can see a form definition is just a normal class defintion.\n    Callbacks can be defined in both the class and the module, the\n    latter is recommended if you want to use the callback function\n    in more than one form.\n\n    Note that there are in fact two base forms. `Form` and\n    `OrderedForm`. The latter knows about the order of the form fields\n    defined in it. Use this if you want to iterate over form fields\n    in templates.\n\n    You can use it inside of the controller like this::\n\n        form = RegisterForm(req, self, \'POST\')\n        # fill with defaults\n        form.fill(defaults)\n        # fill with request data\n        if req.method == \'POST\':\n            form.update(req.form, prefix=\'f_\')\n            if not form.has_errors:\n                # get form data and do something:\n                d = form.to_dict()\n                ...\n        return TemplateResponse(\'name_of_template.html\',\n            form = form.generate(prefix=\'f_\')\n        )\n\n    Templates\n    ---------\n\n    The form templates are very clean and easy since the form fields\n    are able to create the html code of the form fields theirselves.\n    Most request handlers put a variable named ``\'form\'`` into the\n    template context which includes at least the following keys:\n\n    ``action``\n        the target url of the form\n\n    ``method``\n        the method (either ``\'post\'`` or ``\'get\'``)\n\n    If the form is a `OrderedForm` there will be also a key called\n    ``fields`` which is a list of form field items in the correct\n    order so that you can iterate over them.\n\n    The form fields itself are also part of that dict. For example,\n    if your form field is called ``\'foo\'`` you can get access to it\n    by using ``form.foo`` in the template.\n\n    What keys a form field acutally has depends on the type of form\n    field. For a detailed description have a look at the docstrings of\n    the form fields below.\n\n    At least the following keys will be present:\n\n    ``name``\n        the name of the form field\n\n    ``id``\n        the id of the form field\n\n    ``html``\n        generated html markup for the formfield\n\n    ``errors``\n        the rendered partial template ``\'partial/form_errors.html``.\n        (this template is rendered for each form field, the list\n        of errors is in the variable ``errors``)\n\n    ``js``\n        javascript sourcecode for the ajax validator call (already\n        part of the ``html`` value)\n\n    All fields except the `PasswordField` also have a ``value``\n    variable that includes the current value)\n\n    Example Template::\n\n        <dl>\n          <dt>{% trans "Username" %}</dt>\n          <dd>{{ form.username.html }}\n              {{ form.username.errors }}</dd>\n          <dt>{% trans "E-Mail" %}</dt>\n          <dd>{{ form.email.html }}\n              {{ form.email.errors }}</dd>\n          <dt>{% trans "Password" %}</dt>\n          <dd>{{ form.password.html }}\n              {{ form.password.errors }}</dd>\n          <dt>{% trans "Password again" %}</dt>\n          <dd>{{ form.password2.html }}\n              {{ form.password2.errors }}</dd>\n        </dl>\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
from weakref import WeakValueDictionary
from pocoo.template import render_template
from pocoo.utils.html import escape_html
from pocoo.utils.validators import ValidationError, isInChoiceList, isNotMultiline, doMultiCheck
_last_field_id = 0
_last_form_id = 0
_forms = WeakValueDictionary()
JAVASCRIPT_TEMPLATE = '\n<script type="text/javascript">\n  /* do_something_with(\'%(client_id)s\') */\n</script>'

def get_javascript(client_id, form_id, field_id):
    """Return the javascript validator call for a form field."""
    return JAVASCRIPT_TEMPLATE % locals()


def get_form(form_id):
    """Return the form for a given id or `ValueError` if not found."""
    try:
        return _forms[form_id]
    except KeyError:
        raise ValueError('Form %r not found' % form_id)


class FormFieldMeta(type):
    __module__ = __name__

    def __call__(*args, **kwargs):
        global _last_field_id
        formfield = type.__call__(*args, **kwargs)
        formfield._internal_id = _last_field_id
        formfield.server_id = '%x' % _last_field_id
        _last_field_id += 1
        return formfield


class FormField(object):
    """
    Base class for all form fields. It's not possible to generate
    a template context of this abstract form field, so it's required
    to override the `get_template_context` method.
    """
    __module__ = __name__
    __metaclass__ = FormFieldMeta
    bound = False

    def __init__(self, validator=None, manipulator=None):
        self.name = None
        if validator is None:
            validator = lambda x, y: None
        self.validator = validator
        if manipulator is None:
            manipulator = unicode
        self.manipulator = manipulator
        return

    def bind(self, form):
        """Return a bound FormField."""
        assert not self.bound, 'tried to bind a bound form field'
        cls = type('Bound' + self.__class__.__name__, (
         BoundFormField, self.__class__), {})
        result = object.__new__(cls)
        result.__dict__.update(self.__dict__)
        result.form = form
        result.req = form.req
        result.ctx = form.ctx
        result.reset()
        return result

    def reset(self):
        """Reset the form field to defaults."""
        assert self.bound, 'access to unbound form field'
        self.value = ''
        self.errors = []

    def set_value(self, form, data):
        """Set the field value to the data requested"""
        assert self.bound, 'access to unbound form field'
        if data is None:
            self.value = ''
        else:
            self.value = unicode(data)
        return

    def validate(self, form):
        """Validate the formfield"""
        assert self.bound, 'access to unbound form field'
        try:
            self.validator(self, form)
        except ValidationError, e:
            self.errors[:] = e.args
        else:
            self.errors[:] = ()

    def get_template_context(self, form, prefix):
        """Return the template context for this field."""
        assert self.bound, 'access to unbound form field'
        raise NotImplementedError()

    def get_value(self, form):
        """Return the converted value of this field."""
        assert self.bound, 'access to unbound form field'
        if self.errors:
            return self.manipulator()
        return self.manipulator(self.value)

    def get_raw_value(self, form):
        """Return the current form value as unicode object
        so that you can insert it into html code again."""
        if self.value is None:
            return ''
        return unicode(self.value)

    def render_errors(self):
        """Render the partial error template."""
        assert self.bound, 'access to unbound form field'
        return render_template(self.req, 'partial/form_error.html', {'errors': self.errors})

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)


class BoundFormField(FormField):
    """
    Special Class representing bound form fields. This class is
    created by the `bind` method of a `FormField`. You can't
    create instances of this class yourself.
    """
    __module__ = __name__
    __metaclass__ = type
    bound = True

    def __init__(self):
        raise TypeError('cannot create %r instances' % self.__class__.__name__)

    def __repr__(self):
        return '<%s %s: %r>' % (self.__class__.__name__, self.name, self.value)


class FormMeta(type):
    __module__ = __name__

    def __new__(cls, name, bases, d):
        global _last_form_id
        form = type.__new__(cls, name, bases, d)
        form._internal_id = _last_form_id
        form.server_id = '%x' % _last_form_id
        form.fields = fields = []
        form.field_id_map = id_map = {}
        for (key, value) in d.iteritems():
            if isinstance(value, FormField):
                if value.name is not None:
                    raise TypeError("you can't use a form field twice")
                value.form_class = form
                value.name = key
                fields.append(value)
                id_map[value.server_id] = value

        _last_form_id += 1
        _forms[form.server_id] = form
        return form


class OrderedFormMeta(FormMeta):
    __module__ = __name__

    def __new__(cls, name, bases, d):
        form = FormMeta.__new__(cls, name, bases, d)
        form.fields.sort(key=lambda x: x._internal_id)
        return form


class Form(object):
    """
    Basic Form. Allows you to define a bunch of form fields
    as class variables. Each form field must be defined only
    for one form at the same time. It's not possible to pass
    form fields from one from definition to another one.
    """
    __module__ = __name__
    __metaclass__ = FormMeta

    def __init__(self, req, url, method, defaults=None):
        assert method in ('POST', 'GET'), 'method must be either POST or GET'
        self.req = req
        self.ctx = req.ctx
        self.method = method
        if hasattr(url, 'url'):
            self.url = url.url
        else:
            self.url = req.ctx.make_url(url)
        self.has_errors = False
        self.field_map = {}
        fielditer, self.fields = iter(self.fields), []
        for field in fielditer:
            bound_field = field.bind(self)
            self.fields.append(bound_field)
            self.field_map[field.name] = bound_field

        if defaults:
            self.fill(defaults)

    def fill(self, d):
        """
        Fills the form with defaults. The `has_error` value
        is left ontouched. It's also possible to fill the
        form with defaults by using the `defaults` parameter
        of the constructor.
        """
        for field in self.fields:
            if field.name in d:
                field.set_value(self, d[field.name])

    def update(self, d, prefix=''):
        """
        This method updates the form values of each field
        and calls the validators afterwards.
        """
        for field in self.fields:
            key = prefix + field.name
            if key in d:
                field.set_value(self, d[key])
            elif isinstance(field, CheckBox):
                field.set_value(self, False)

        for field in self.fields:
            field.validate(self)
            if field.errors:
                self.has_errors = True

    def reset(self):
        """Reset the form"""
        for field in self.fields:
            field.reset()

        self.has_errors = False

    def to_dict(self):
        """
        Collect all values from the fields and apply the manipulators.
        The return value is a dictionary.
        """
        return dict(((field.name, field.get_value(self)) for field in self.fields))

    def generate(self, prefix=''):
        """
        This method generates a dict which is meant to be passed to the
        template context. The keys of this dict are the names of the
        form fields. Additionally the keys ``'action'`` and ``'method'``
        (which held the url and the transport method) exists. If those
        collide with names of the form fields, the form field names
        are renamed so that they have a trailing underscore in the name.
        """
        result = {}
        for field in self.fields:
            name = field.name
            if name in ('action', 'method'):
                name += '_'
            result[name] = field.get_template_context(self, prefix)

        result['action'] = self.url
        result['method'] = self.method.lower()
        return result


class OrderedForm(Form):
    """
    Works pretty much like the normal form, except that the
    form fields are stored on the form in the order they
    appear in the sourcecode. To get the correct field order
    in the template use the ``form.fields`` variable which is
    an iterable of form fields.
    """
    __module__ = __name__
    __metaclass__ = OrderedFormMeta

    def generate(self, prefix=''):
        """
        Works like the `generate` method of the normal `Form` class
        except that the fields are in the dict twice. A second time
        in the ordered list ``'fields'`` so that a template designer
        can iterate over the list.
        """
        result = {}
        fields = []
        for field in self.fields:
            name = field.name
            if name in ('action', 'method', 'fields'):
                name += '_'
            result[name] = f = field.get_template_context(self, prefix)
            fields.append(f)

        result['fields'] = fields
        result['action'] = self.url
        result['method'] = self.method.lower()
        return result

    def to_list(self):
        """
        Works like `to_dict` but it returns an ordered list of
        ``(name, value)`` tuples.
        """
        return [ (field.name, field.get_value(self)) for field in self.fields ]


class TextField(FormField):
    __module__ = __name__

    def __init__(self, validator=None, manipulator=None):
        if validator is None:
            validator = isNotMultiline()
        else:
            validator = doMultiCheck(isNotMultiline(), validator)
        super(TextField, self).__init__(validator, manipulator)
        return

    def get_template_context(self, form, prefix):
        assert self.bound, 'access to unbound form field'
        name = prefix + self.name
        js = get_javascript(name, form.server_id, self.server_id)
        return {'name': name, 'id': name, 'server_id': self.server_id, 'value': self.value, 'errors': self.render_errors(), 'js': js, 'html': '<input name="%s" id="%s" value="%s" />%s' % (name, name, escape_html(self.get_raw_value(form)), js)}


class PasswordField(TextField):
    __module__ = __name__

    def get_template_context(self, form, prefix):
        assert self.bound, 'access to unbound form field'
        name = prefix + self.name
        js = get_javascript(name, form.server_id, self.server_id)
        return {'name': prefix + self.name, 'id': name, 'server_id': self.server_id, 'errors': self.render_errors(), 'js': js, 'html': '<input type="password" name="%s" id="%s" />%s' % (name, name, js)}


class HiddenField(FormField):
    __module__ = __name__

    def __init__(self, manipulator=None):
        FormField.__init__(self, None, manipulator)
        return

    def validate(self, form):
        """Validate the formfield"""
        assert self.bound, 'access to unbound form field'
        try:
            self.manipulator(self.value)
        except ValueError, e:
            self.errors[:] = ('Hacking Attempt', )

    def get_template_context(self, form, prefix):
        assert self.bound, 'access to unbound form field'
        name = prefix + self.name
        return {'name': name, 'value': self.value, 'html': '<input type="hidden" name="%s" value="%s" />' % (name, escape_html(self.get_raw_value(form)))}


class TextArea(FormField):
    __module__ = __name__

    def get_template_context(self, form, prefix):
        assert self.bound, 'access to unbound form field'
        name = prefix + self.name
        js = get_javascript(name, form.server_id, self.server_id)
        return {'name': name, 'id': name, 'server_id': self.server_id, 'value': self.value, 'errors': self.render_errors(), 'js': js, 'html': '<textarea name="%s" id="%s">%s</textarea>%s' % (name, name, escape_html(self.get_raw_value(form)), js)}


class FileField(FormField):
    __module__ = __name__

    def get_template_context(self, form, prefix):
        assert self.bound, 'access to unbound form field'
        name = prefix + self.name
        js = get_javascript(name, form.server_id, self.server_id)
        return {'name': name, 'id': name, 'server_id': self.server_id, 'errors': self.render_errors(), 'js': js, 'html': '<input type="file" name="%s" id="%s" />%s' % (name, name, js)}


class CheckBox(FormField):
    __module__ = __name__

    def __init__(self, validator=None, manipulator=None):

        def checkbox_manipulator(x):
            if isinstance(x, unicode):
                return True
            else:
                return False

        if manipulator is None:
            manipulator = checkbox_manipulator
        super(CheckBox, self).__init__(validator, manipulator)
        return

    def get_value(self, form):
        assert self.bound, 'access to unbound form field'
        return self.manipulator(self.value)

    def get_template_context(self, form, prefix):
        assert self.bound, 'access to unbound form field'
        name = prefix + self.name
        js = get_javascript(name, form.server_id, self.server_id)
        return {'name': name, 'id': name, 'server_id': self.server_id, 'checked': bool(self.value), 'errors': self.render_errors(), 'js': js, 'html': '<input type="checkbox" value="on"name="%s" id="%s"%s />%s' % (name, name, bool(self.value) and ' checked="checked"' or '', js)}


class SelectBox(FormField):
    __module__ = __name__

    def __init__(self, choices_callback, validator=None, manipulator=None):
        self.choices_callback = choices_callback
        super(SelectBox, self).__init__(validator, manipulator)

    def validate(self, form):
        assert self.bound, 'access to unbound form field'
        choices = self.choices_callback(self, form)
        if isinstance(choices, dict):
            choices = choices.keys()
        else:
            choices = [ x[0] for x in choices ]
        validator = doMultiCheck(isInChoiceList(choices), self.validator)
        try:
            validator(self, form)
        except ValidationError, e:
            self.errors[:] = e.args
        else:
            self.errors[:] = ()

    def get_template_context(self, form, prefix):
        assert self.bound, 'access to unbound form field'
        choices = self.choices_callback(self, form)
        if isinstance(choices, dict):
            choices = choices.items()
            choices.sort(key=lambda x: x[1].lower())
        values = []
        name = prefix + self.name
        js = get_javascript(name, form.server_id, self.server_id)
        for (value, caption) in choices:
            values.append({'value': value, 'caption': caption, 'selected': value == self.value})

        return {'name': name, 'id': name, 'server_id': self.server_id, 'values': values, 'errors': self.render_errors(), 'js': js, 'html': '<select name="%s" id="%s">%s</select>%s' % (name, name, ('\n').join(('<option value="%s"%s>%s</option>' % (escape_html(item['value']), item['selected'] and ' selected="selected"' or '', escape_html(item['caption'])) for item in values)), js)}