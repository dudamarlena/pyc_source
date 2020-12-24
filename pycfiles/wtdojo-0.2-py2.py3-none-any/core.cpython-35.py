# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/wtdojo/wtdojo/widgets/core.py
# Compiled at: 2015-09-12 14:06:12
# Size of source mod 2**32: 7672 bytes
from cgi import escape
from wtforms.compat import text_type, string_types, iteritems
from wtforms.widgets import CheckboxInput, FileInput, HiddenInput, ListWidget, PasswordInput, RadioInput, Select, SubmitInput, TableWidget, TextArea, TextInput, Option
from wtforms.widgets.core import html_params, HTMLString
from ..validators import get_validation_str
__all__ = ('DojoInput', 'DojoTextInput', 'DojoValidationTextBox', 'DojoDateTextBox',
           'DojoTimeTextBox', 'DojoPasswordBox', 'DojoTextArea', 'DojoSimpleTextArea',
           'DojoNumbertextBox', 'DojoNumberSpinner', 'DojoFilteringSelect', 'DojoMultiSelect',
           'DojoCheckBox')

class DojoInput(object):
    __doc__ = '\n    Render a basic ``<input>`` field.\n\n    This is used as the basis for most of the other input fields.\n\n    By default, the `_value()` method will be called upon the associated field\n    to provide the ``value=`` HTML attribute.\n    '
    html_params = staticmethod(html_params)

    def __init__(self, input_type=None, dojo_type=None):
        if input_type is not None:
            self.input_type = input_type
        if dojo_type is not None:
            self.dojo_type = dojo_type

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('data-dojo-type', self.dojo_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        return HTMLString('<input %s>' % self.html_params(name=field.name, **kwargs))


class DojoTextBox(DojoInput):
    __doc__ = '\n    Render a single-line text input.\n    '
    input_type = 'text'
    dojo_type = 'dijit/form/TextBox'


class DojoValidationTextBox(DojoInput):
    __doc__ = '\n    Render a single-line text input with validation support for WTForms fields.\n    '
    input_type = 'text'
    dojo_type = 'dijit/form/ValidationTextBox'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('data-dojo-type', self.dojo_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        return HTMLString('<input %s %s>' % (get_validation_str(field),
         self.html_params(name=field.name, **kwargs)))


class DojoNumberTextBox(DojoValidationTextBox):
    __doc__ = '\n    Render a single-line text input that only accepts numbers.\n    '
    input_type = 'text'
    dojo_type = 'dijit/form/NumberTextBox'


class DojoNumberSpinner(DojoValidationTextBox):
    __doc__ = '\n    Render a number spinner to select a value\n    '
    input_type = 'text'
    dojo_type = 'dijit/form/NumberSpinner'


class DojoDateTextBox(DojoValidationTextBox):
    __doc__ = '\n    Render a single-line text input.\n    '
    input_type = 'text'
    dojo_type = 'dijit/form/DateTextBox'


class DojoTimeTextBox(DojoValidationTextBox):
    __doc__ = '\n    Render a single-line text input.\n    '
    input_type = 'text'
    dojo_type = 'dijit/form/TimeTextBox'


class DojoPasswordBox(DojoValidationTextBox):
    __doc__ = '\n    Render a single-line password input.\n    '
    input_type = 'password'

    def __init__(self, hide_value=True):
        self.hide_value = hide_value

    def __call__(self, field, **kwargs):
        if self.hide_value:
            kwargs['value'] = ''
        return super(DojoPasswordBox, self).__call__(field, **kwargs)


class DojoTextArea(DojoInput):
    __doc__ = '\n    Renders a multi-line text area that automatically expands when more content is added to it.\n\n    `rows` and `cols` ought to be passed as keyword args when rendering.\n    '
    dojo_type = 'dijit/form/Textarea'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('data-dojo-type', self.dojo_type)
        return HTMLString('<textarea %s %s>%s</textarea>' % (html_params(name=field.name, **kwargs),
         get_validation_str(field),
         escape(text_type(field._value()))))


class DojoSimpleTextArea(DojoInput):
    __doc__ = '\n    Renders a multi-line text area.\n\n    `rows` and `cols` ought to be passed as keyword args when rendering.\n    '
    dojo_type = 'dijit/form/SimpleTextarea'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('data-dojo-type', self.dojo_type)
        return HTMLString('<textarea %s %s>%s</textarea>' % (html_params(name=field.name, **kwargs),
         get_validation_str(field),
         escape(text_type(field._value()))))


class DojoCheckBox(DojoInput):
    __doc__ = "\n    Render a checkbox.\n\n    The ``checked`` HTML attribute is set if the field's data is a non-false value.\n    "
    input_type = 'checkbox'
    dojo_type = 'dijit/form/CheckBox'

    def __call__(self, field, **kwargs):
        if getattr(field, 'checked', field.data):
            kwargs['checked'] = True
        return super(DojoCheckBox, self).__call__(field, **kwargs)


class DojoFilteringSelect(Select):
    __doc__ = '\n    Renders a Dojo Filtering Select widget.\n\n    The field must provide an `iter_choices()` method which the widget will\n    call on rendering; this method must yield tuples of\n    `(value, label, selected)`.\n    '
    dojo_type = 'dijit/form/FilteringSelect'

    def __init__(self, input_type=None, dojo_type=None):
        if dojo_type is not None:
            self.dojo_type = dojo_type

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('data-dojo-type', self.dojo_type)
        html = [
         '<select %s>' % html_params(name=field.name, **kwargs)]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))

        html.append('</select>')
        return HTMLString(''.join(html))


class DojoMultiSelect(DojoFilteringSelect):
    __doc__ = '\n    Renders a Dojo Multi Select widget.\n\n    The `size` property should be specified on\n    rendering to make the field useful.\n\n    The field must provide an `iter_choices()` method which the widget will\n    call on rendering; this method must yield tuples of\n    `(value, label, selected)`.\n    '
    dojo_type = 'dijit/form/MultiSelect'