# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/form.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.utils.form\n    ~~~~~~~~~~~~~~~~\n\n    Pocoo form validation helpers.\n\n\n    Form Validation\n    ===============\n\n    Validating forms sucks. To simplify it, Pocoo provides some classes\n    for form validation.\n\n\n    Application Side\n    ----------------\n\n    Real-world usage example::\n\n        from pocoo.application import RequestHandler\n        from pocoo.template import TemplateResponse\n        from pocoo.utils.form import Form, TextField, TextArea\n        from pocoo.utils import validators as V\n\n        class NewThread(RequestHandler):\n\n            def get_handler_regexes(self):\n                yield r\'forum/(?P<id>\\d+)/new$\'\n\n            def handle_request(self, req, forum_id):\n                form = Form(req, \'forum/%d/new\' % forum.forum_id, \'POST\',\n                    TextField(\'title\', validator=V.checkTextLength(3, 60)),\n                    TextArea(\'text\', validator=V.checkTextLength(4, 3000))\n                )\n                if \'sent\' in req.form:\n                    form.update(req.form, prefix=\'f_\')\n                    if not form.has_errors:\n                        d = form.to_dict()\n                        # do something with the form data dict "d"\n                return TemplateResponse(\'posting\',\n                    forum=forum,\n                    form=form.generate(prefix=\'f_\')\n                )\n\n    **Note:** Validators are either classes or functions. In the module\n    definition, they must have a pep8 conform name, but get a ``smallCaps``\n    name after having been assigned to the ``Form`` class.\n\n    Manipulators\n    ------------\n\n    The data returned from ``form.to_dict()`` normally is just a string.\n    But if the form contains no errors the manipulators are called. A\n    manipulator is a callable that returns something. You can use the builtin\n    python types ``str``, ``int``, ``unicode``, ``float`` or ``bool``::\n\n        form = Form(req, \'test\', \'POST\',\n           TextField(\'a_number\', validator=v.isInteger(), manipulator=int)\n        )\n        form.update(req.form)\n        if not form.has_errors:\n            d = form.to_dict()\n            n = d[\'a_number\']\n            print \'%d + 4 = %d\' % (n, n + 4)\n        else:\n            print \'wrong data\'\n\n    Template Usage\n    --------------\n\n    ::\n\n        <form action="{{ form.action }}" method="{{ form.method }}">\n          {% if form.errors %}\n          <div class="error">\n            {% trans "There are some errors in your form" %}\n          </div>\n          {% endif %}\n\n          <input type="text" name="{{ form.title.name }}"\n                 value="{{ form.title.value|e }}" />\n          {% if form.title.errors %}\n          <ul class="error">\n            {% for error in form.title.errors %}\n            <li>{{ error|e }}</li>\n            {% endfor %}\n          </ul>\n          {% endif %}\n\n          <textarea name="{{ form.text.name }}">{{ form.text.value|e }}</textarea>\n          {% if form.text.errors %}\n          <ul class="error">\n            {% for error in form.text.errors %}\n            <li>{{ error|e }}</li>\n            {% endfor %}\n          </ul>\n          {% endif %}\n        </form>\n\n    Each `FormField` returns a different template context. `TextField` and\n    `TextArea` provide ``name`` and ``value``. `SelectBox` provides ``name``,\n    ``values`` where ``values`` is a list of dicts in the form\n    ``{\'active\': bool, \'value\': str, \'caption\': str}``::\n\n        <select name="{{ form.timezone }}">\n        {% for item in form.timezone.values %}\n          <option value="{{ item.value|e }}"\n              {% if item.active %} selected="selected"{% endif %}>\n            {{ item.caption|e }}</option>\n        {% endfor %}\n        </select>\n\n    A `CheckBox` works like a `TextField` or `TextArea` but also provides\n    a checked key in the context.\n\n    Validators\n    ----------\n\n    Core validators are defined in `pocoo.utils.validators` and\n    `pocoo.pkg.core.validators`.\n\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
from pocoo.utils.validators import ValidationError, isInChoiceList, isNotMultiline, doMultiCheck

class Form(object):
    __module__ = __name__

    def __init__(self, req, url, method, *fields):
        assert method in ('POST', 'GET'), 'method must be either POST or GET'
        self.req = req
        self.method = method
        if hasattr(url, 'url'):
            self.url = url.url
        else:
            self.url = req.ctx.make_url(url)
        self.fields = {}
        for field in fields:
            self.fields[field.name] = field

        self.has_errors = False

    def __getitem__(self, key):
        return self.fields[key]

    def update(self, d, prefix=''):
        for (name, field) in self.fields.iteritems():
            key = prefix + name
            if key in d:
                field.set_value(self, d[key])
            elif isinstance(field, CheckBox):
                field.set_value(self, False)

        for field in self.fields.itervalues():
            field.validate(self)
            if field.errors:
                self.has_errors = True

    def reset(self):
        self.has_errors = False

    def to_dict(self):
        return dict(((name, field.get_value(self)) for (name, field) in self.fields.iteritems()))

    def generate(self, prefix=''):
        result = {}
        for (name, field) in self.fields.iteritems():
            if name in ('action', 'method'):
                name += '_'
            result[name] = field.get_template_context(self, prefix)

        result['action'] = self.url
        result['method'] = self.method.lower()
        return result


class FormField(object):
    __module__ = __name__

    def __init__(self, name, default='', validator=None, manipulator=None):
        self.name = name
        self.value = default
        if validator is None:
            validator = lambda x, y: None
        self.validator = validator
        if manipulator is None:
            manipulator = unicode
        self.manipulator = manipulator
        self.errors = []
        return

    def set_value(self, form, data):
        self.value = data

    def validate(self, form):
        try:
            self.validator(self, form)
        except ValidationError, e:
            self.errors[:] = e.args
        else:
            self.errors[:] = ()

    def get_template_context(self, form, prefix):
        raise NotImplementedError()

    def get_value(self, form):
        if self.errors:
            return self.manipulator()
        return self.manipulator(self.value)

    def __repr__(self):
        return '<%s %s: %r>' % (self.__class__.__name__, self.name, self.value)


class TextField(FormField):
    __module__ = __name__

    def __init__(self, name, default='', validator=None, manipulator=None):
        if validator is None:
            validator = isNotMultiline()
        else:
            validator = doMultiCheck(isNotMultiline(), validator)
        super(TextField, self).__init__(name, default, validator, manipulator)
        return

    def get_template_context(self, form, prefix):
        return {'name': prefix + self.name, 'value': self.value, 'errors': self.errors}


class TextArea(FormField):
    __module__ = __name__

    def get_template_context(self, form, prefix):
        return {'name': prefix + self.name, 'value': self.value, 'errors': self.errors}


class FileField(FormField):
    __module__ = __name__

    def get_template_context(self, form, prefix):
        return {'name': prefix + self.name, 'errors': self.errors}


class CheckBox(FormField):
    __module__ = __name__

    def __init__(self, name, default=False, validator=None, manipulator=None):

        def checkbox_manipulator(x):
            if isinstance(x, unicode):
                return True
            else:
                return False

        if manipulator is None:
            manipulator = checkbox_manipulator
        super(CheckBox, self).__init__(name, default, validator, manipulator)
        return

    def get_value(self, form):
        return self.manipulator(self.value)

    def get_template_context(self, form, prefix):
        return {'name': prefix + self.name, 'checked': bool(self.value), 'value': self.value}


class SelectBox(FormField):
    __module__ = __name__

    def __init__(self, name, choices, default='', validator=None, manipulator=None):
        if isinstance(choices, dict):
            self.choices = sorted(choices.items())
        else:
            self.choices = choices
        choices = [ item for (item, _) in self.choices ]
        if validator is None:
            validator = isInChoiceList(choices)
        else:
            validator = doMultiCheck(isInChoiceList(choices), validator)
        super(SelectBox, self).__init__(name, default, validator, manipulator)
        return

    def get_template_context(self, form, prefix):
        values = []
        for item in self.choices:
            if isinstance(item, (tuple, list)):
                values.append({'value': item[0], 'caption': item[1], 'selected': item[0] == self.value})
            else:
                values.append({'value': item, 'caption': item, 'selected': item == self.value})

        return {'name': prefix + self.name, 'values': values, 'errors': self.errors}