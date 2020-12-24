# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/forms/forms.py
# Compiled at: 2019-02-14 00:35:17
"""
Form classes
"""
from __future__ import unicode_literals
import copy
from collections import OrderedDict
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms.boundfield import BoundField
from django.forms.fields import Field, FileField
from django.forms.utils import ErrorDict, ErrorList, pretty_name
from django.forms.widgets import Media, MediaDefiningClass
from django.utils import six
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.html import conditional_escape, html_safe
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from .renderers import get_default_renderer
__all__ = (
 b'BaseForm', b'Form')

class DeclarativeFieldsMetaclass(MediaDefiningClass):
    """
    Metaclass that collects Fields declared on the base classes.
    """

    def __new__(mcs, name, bases, attrs):
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                current_fields.append((key, value))
                attrs.pop(key)

        current_fields.sort(key=lambda x: x[1].creation_counter)
        attrs[b'declared_fields'] = OrderedDict(current_fields)
        new_class = super(DeclarativeFieldsMetaclass, mcs).__new__(mcs, name, bases, attrs)
        declared_fields = OrderedDict()
        for base in reversed(new_class.__mro__):
            if hasattr(base, b'declared_fields'):
                declared_fields.update(base.declared_fields)
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields
        return new_class


@html_safe
@python_2_unicode_compatible
class BaseForm(object):
    default_renderer = None
    field_order = None
    prefix = None
    use_required_attribute = True

    def __init__(self, data=None, files=None, auto_id=b'id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None, renderer=None):
        self.is_bound = data is not None or files is not None
        self.data = data or {}
        self.files = files or {}
        self.auto_id = auto_id
        if prefix is not None:
            self.prefix = prefix
        self.initial = initial or {}
        self.error_class = error_class
        self.label_suffix = label_suffix if label_suffix is not None else _(b':')
        self.empty_permitted = empty_permitted
        self._errors = None
        self.fields = copy.deepcopy(self.base_fields)
        self._bound_fields_cache = {}
        self.order_fields(self.field_order if field_order is None else field_order)
        if use_required_attribute is not None:
            self.use_required_attribute = use_required_attribute
        if renderer is None:
            if self.default_renderer is None:
                renderer = get_default_renderer()
            else:
                renderer = self.default_renderer
                if isinstance(self.default_renderer, type):
                    renderer = renderer()
        self.renderer = renderer
        return

    def order_fields(self, field_order):
        """
        Rearranges the fields according to field_order.

        field_order is a list of field names specifying the order. Fields not
        included in the list are appended in the default order for backward
        compatibility with subclasses not overriding field_order. If field_order
        is None, all fields are kept in the order defined in the class.
        Unknown fields in field_order are ignored to allow disabling fields in
        form subclasses without redefining ordering.
        """
        if field_order is None:
            return
        else:
            fields = OrderedDict()
            for key in field_order:
                try:
                    fields[key] = self.fields.pop(key)
                except KeyError:
                    pass

            fields.update(self.fields)
            self.fields = fields
            return

    def __str__(self):
        return self.as_table()

    def __repr__(self):
        if self._errors is None:
            is_valid = b'Unknown'
        else:
            is_valid = self.is_bound and not bool(self._errors)
        return b'<%(cls)s bound=%(bound)s, valid=%(valid)s, fields=(%(fields)s)>' % {b'cls': self.__class__.__name__, 
           b'bound': self.is_bound, 
           b'valid': is_valid, 
           b'fields': (b';').join(self.fields)}

    def __iter__(self):
        for name in self.fields:
            yield self[name]

    def __getitem__(self, name):
        """Returns a BoundField with the given name."""
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError(b"Key '%s' not found in '%s'. Choices are: %s." % (
             name,
             self.__class__.__name__,
             (b', ').join(sorted(f for f in self.fields))))

        if name not in self._bound_fields_cache:
            self._bound_fields_cache[name] = field.get_bound_field(self, name)
        return self._bound_fields_cache[name]

    @property
    def errors(self):
        """Returns an ErrorDict for the data provided for the form"""
        if self._errors is None:
            self.full_clean()
        return self._errors

    def is_valid(self):
        """
        Returns True if the form has no errors. Otherwise, False. If errors are
        being ignored, returns False.
        """
        return self.is_bound and not self.errors

    def add_prefix(self, field_name):
        """
        Returns the field name with a prefix appended, if this Form has a
        prefix set.

        Subclasses may wish to override.
        """
        if self.prefix:
            return b'%s-%s' % (self.prefix, field_name)
        return field_name

    def add_initial_prefix(self, field_name):
        """
        Add a 'initial' prefix for checking dynamic initial values
        """
        return b'initial-%s' % self.add_prefix(field_name)

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        """Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."""
        top_errors = self.non_field_errors()
        output, hidden_fields = [], []
        for name, field in self.fields.items():
            html_class_attr = b''
            bf = self[name]
            bf_errors = self.error_class([ conditional_escape(error) for error in bf.errors ])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([ _(b'(Hidden field %(name)s) %(error)s') % {b'name': name, b'error': force_text(e)} for e in bf_errors
                                      ])
                hidden_fields.append(six.text_type(bf))
            else:
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = b' class="%s"' % css_classes
                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_text(bf_errors))
                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    label = bf.label_tag(label) or b''
                else:
                    label = b''
                if field.help_text:
                    help_text = help_text_html % force_text(field.help_text)
                else:
                    help_text = b''
                output.append(normal_row % {b'errors': force_text(bf_errors), 
                   b'label': force_text(label), 
                   b'field': six.text_type(bf), 
                   b'help_text': help_text, 
                   b'html_class_attr': html_class_attr, 
                   b'css_classes': css_classes, 
                   b'field_name': bf.html_name})

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))
        if hidden_fields:
            str_hidden = (b'').join(hidden_fields)
            if output:
                last_row = output[(-1)]
                if not last_row.endswith(row_ender):
                    last_row = normal_row % {b'errors': b'', 
                       b'label': b'', 
                       b'field': b'', 
                       b'help_text': b'', 
                       b'html_class_attr': html_class_attr, 
                       b'css_classes': b'', 
                       b'field_name': b''}
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                output.append(str_hidden)
        return mark_safe((b'\n').join(output))

    def as_table(self):
        """Returns this form rendered as HTML <tr>s -- excluding the <table></table>."""
        return self._html_output(normal_row=b'<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>', error_row=b'<tr><td colspan="2">%s</td></tr>', row_ender=b'</td></tr>', help_text_html=b'<br /><span class="helptext">%s</span>', errors_on_separate_row=False)

    def as_ul(self):
        """Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."""
        return self._html_output(normal_row=b'<li%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</li>', error_row=b'<li>%s</li>', row_ender=b'</li>', help_text_html=b' <span class="helptext">%s</span>', errors_on_separate_row=False)

    def as_p(self):
        """Returns this form rendered as HTML <p>s."""
        return self._html_output(normal_row=b'<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>', error_row=b'%s', row_ender=b'</p>', help_text_html=b' <span class="helptext">%s</span>', errors_on_separate_row=True)

    def non_field_errors(self):
        """
        Returns an ErrorList of errors that aren't associated with a particular
        field -- i.e., from Form.clean(). Returns an empty ErrorList if there
        are none.
        """
        return self.errors.get(NON_FIELD_ERRORS, self.error_class(error_class=b'nonfield'))

    def add_error(self, field, error):
        """
        Update the content of `self._errors`.

        The `field` argument is the name of the field to which the errors
        should be added. If its value is None the errors will be treated as
        NON_FIELD_ERRORS.

        The `error` argument can be a single error, a list of errors, or a
        dictionary that maps field names to lists of errors. What we define as
        an "error" can be either a simple string or an instance of
        ValidationError with its message attribute set and what we define as
        list or dictionary can be an actual `list` or `dict` or an instance
        of ValidationError with its `error_list` or `error_dict` attribute set.

        If `error` is a dictionary, the `field` argument *must* be None and
        errors will be added to the fields that correspond to the keys of the
        dictionary.
        """
        if not isinstance(error, ValidationError):
            error = ValidationError(error)
        if hasattr(error, b'error_dict'):
            if field is not None:
                raise TypeError(b'The argument `field` must be `None` when the `error` argument contains errors for multiple fields.')
            else:
                error = error.error_dict
        else:
            error = {field or NON_FIELD_ERRORS: error.error_list}
        for field, error_list in error.items():
            if field not in self.errors:
                if field != NON_FIELD_ERRORS and field not in self.fields:
                    raise ValueError(b"'%s' has no field named '%s'." % (self.__class__.__name__, field))
                if field == NON_FIELD_ERRORS:
                    self._errors[field] = self.error_class(error_class=b'nonfield')
                else:
                    self._errors[field] = self.error_class()
            self._errors[field].extend(error_list)
            if field in self.cleaned_data:
                del self.cleaned_data[field]

        return

    def has_error(self, field, code=None):
        if code is None:
            return field in self.errors
        else:
            if field in self.errors:
                for error in self.errors.as_data()[field]:
                    if error.code == code:
                        return True

            return False

    def full_clean(self):
        """
        Cleans all of self.data and populates self._errors and
        self.cleaned_data.
        """
        self._errors = ErrorDict()
        if not self.is_bound:
            return
        self.cleaned_data = {}
        if self.empty_permitted and not self.has_changed():
            return
        self._clean_fields()
        self._clean_form()
        self._post_clean()

    def _clean_fields(self):
        for name, field in self.fields.items():
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, b'clean_%s' % name):
                    value = getattr(self, b'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self.add_error(name, e)

    def _clean_form(self):
        try:
            cleaned_data = self.clean()
        except ValidationError as e:
            self.add_error(None, e)

        if cleaned_data is not None:
            self.cleaned_data = cleaned_data
        return

    def _post_clean(self):
        """
        An internal hook for performing additional cleaning after form cleaning
        is complete. Used for model validation in model forms.
        """
        pass

    def clean(self):
        """
        Hook for doing any extra form-wide cleaning after Field.clean() has been
        called on every field. Any ValidationError raised by this method will
        not be associated with a particular field; it will have a special-case
        association with the field named '__all__'.
        """
        return self.cleaned_data

    def has_changed(self):
        """
        Returns True if data differs from initial.
        """
        return bool(self.changed_data)

    @cached_property
    def changed_data(self):
        data = []
        for name, field in self.fields.items():
            prefixed_name = self.add_prefix(name)
            data_value = field.widget.value_from_datadict(self.data, self.files, prefixed_name)
            if not field.show_hidden_initial:
                initial_value = self[name].initial
            else:
                initial_prefixed_name = self.add_initial_prefix(name)
                hidden_widget = field.hidden_widget()
                try:
                    initial_value = field.to_python(hidden_widget.value_from_datadict(self.data, self.files, initial_prefixed_name))
                except ValidationError:
                    data.append(name)
                    continue

            if field.has_changed(initial_value, data_value):
                data.append(name)

        return data

    @property
    def media(self):
        """
        Provide a description of all media required to render the widgets on this form
        """
        media = Media()
        for field in self.fields.values():
            media = media + field.widget.media

        return media

    def is_multipart(self):
        """
        Returns True if the form needs to be multipart-encoded, i.e. it has
        FileInput. Otherwise, False.
        """
        for field in self.fields.values():
            if field.widget.needs_multipart_form:
                return True

        return False

    def hidden_fields(self):
        """
        Returns a list of all the BoundField objects that are hidden fields.
        Useful for manual form layout in templates.
        """
        return [ field for field in self if field.is_hidden ]

    def visible_fields(self):
        """
        Returns a list of BoundField objects that aren't hidden fields.
        The opposite of the hidden_fields() method.
        """
        return [ field for field in self if not field.is_hidden ]

    def get_initial_for_field(self, field, field_name):
        """
        Return initial data for field on form. Use initial data from the form
        or the field, in that order. Evaluate callable values.
        """
        value = self.initial.get(field_name, field.initial)
        if callable(value):
            value = value()
        return value


class Form(six.with_metaclass(DeclarativeFieldsMetaclass, BaseForm)):
    """A collection of Fields, plus their associated data."""
    pass