# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/forms/widgets.py
# Compiled at: 2018-07-11 18:15:30
"""
HTML Widget classes
"""
from __future__ import absolute_import, unicode_literals
import copy, datetime
from itertools import chain
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from django.conf import settings
from django.forms.util import flatatt, to_current_timezone
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.translation import ugettext, ugettext_lazy
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils import datetime_safe, formats, six
__all__ = ('Media', 'MediaDefiningClass', 'Widget', 'TextInput', 'PasswordInput', 'HiddenInput',
           'MultipleHiddenInput', 'ClearableFileInput', 'FileInput', 'DateInput',
           'DateTimeInput', 'TimeInput', 'Textarea', 'CheckboxInput', 'Select', 'NullBooleanSelect',
           'SelectMultiple', 'RadioSelect', 'CheckboxSelectMultiple', 'MultiWidget',
           'SplitDateTimeWidget')
MEDIA_TYPES = ('css', 'js')

@python_2_unicode_compatible
class Media(object):

    def __init__(self, media=None, **kwargs):
        if media:
            media_attrs = media.__dict__
        else:
            media_attrs = kwargs
        self._css = {}
        self._js = []
        for name in MEDIA_TYPES:
            getattr(self, b'add_' + name)(media_attrs.get(name, None))

        return

    def __str__(self):
        return self.render()

    def render(self):
        return mark_safe((b'\n').join(chain(*[ getattr(self, b'render_' + name)() for name in MEDIA_TYPES ])))

    def render_js(self):
        return [ format_html(b'<script type="text/javascript" src="{0}"></script>', self.absolute_path(path)) for path in self._js ]

    def render_css(self):
        media = sorted(self._css.keys())
        return chain(*[ [ format_html(b'<link href="{0}" type="text/css" media="{1}" rel="stylesheet" />', self.absolute_path(path), medium) for path in self._css[medium] ] for medium in media
                      ])

    def absolute_path(self, path, prefix=None):
        if path.startswith(('http://', 'https://', '/')):
            return path
        else:
            if prefix is None:
                if settings.STATIC_URL is None:
                    prefix = settings.MEDIA_URL
                else:
                    prefix = settings.STATIC_URL
            return urljoin(prefix, path)

    def __getitem__(self, name):
        """Returns a Media object that only contains media of the given type"""
        if name in MEDIA_TYPES:
            return Media(**{str(name): getattr(self, b'_' + name)})
        raise KeyError(b'Unknown media type "%s"' % name)

    def add_js(self, data):
        if data:
            for path in data:
                if path not in self._js:
                    self._js.append(path)

    def add_css(self, data):
        if data:
            for medium, paths in data.items():
                for path in paths:
                    if not self._css.get(medium) or path not in self._css[medium]:
                        self._css.setdefault(medium, []).append(path)

    def __add__(self, other):
        combined = Media()
        for name in MEDIA_TYPES:
            getattr(combined, b'add_' + name)(getattr(self, b'_' + name, None))
            getattr(combined, b'add_' + name)(getattr(other, b'_' + name, None))

        return combined


def media_property(cls):

    def _media(self):
        sup_cls = super(cls, self)
        try:
            base = sup_cls.media
        except AttributeError:
            base = Media()

        definition = getattr(cls, b'Media', None)
        if definition:
            extend = getattr(definition, b'extend', True)
            if extend:
                if extend == True:
                    m = base
                else:
                    m = Media()
                    for medium in extend:
                        m = m + base[medium]

                return m + Media(definition)
            return Media(definition)
        else:
            return base
        return

    return property(_media)


class MediaDefiningClass(type):
    """Metaclass for classes that can have media definitions"""

    def __new__(cls, name, bases, attrs):
        new_class = super(MediaDefiningClass, cls).__new__(cls, name, bases, attrs)
        if b'media' not in attrs:
            new_class.media = media_property(new_class)
        return new_class


@python_2_unicode_compatible
class SubWidget(object):
    """
    Some widgets are made of multiple HTML elements -- namely, RadioSelect.
    This is a class that represents the "inner" HTML element of a widget.
    """

    def __init__(self, parent_widget, name, value, attrs, choices):
        self.parent_widget = parent_widget
        self.name, self.value = name, value
        self.attrs, self.choices = attrs, choices

    def __str__(self):
        args = [
         self.name, self.value, self.attrs]
        if self.choices:
            args.append(self.choices)
        return self.parent_widget.render(*args)


class Widget(six.with_metaclass(MediaDefiningClass)):
    is_hidden = False
    needs_multipart_form = False
    is_localized = False
    is_required = False

    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
        return

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.attrs = self.attrs.copy()
        memo[id(self)] = obj
        return obj

    def subwidgets(self, name, value, attrs=None, choices=()):
        """
        Yields all "subwidgets" of this widget. Used only by RadioSelect to
        allow template access to individual <input type="radio"> buttons.

        Arguments are the same as for render().
        """
        yield SubWidget(self, name, value, attrs, choices)

    def render(self, name, value, attrs=None):
        """
        Returns this Widget rendered as HTML, as a Unicode string.

        The 'value' given is not guaranteed to be valid input, so subclass
        implementations should program defensively.
        """
        raise NotImplementedError

    def build_attrs(self, extra_attrs=None, **kwargs):
        """Helper function for building an attribute dictionary."""
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        return data.get(name, None)

    def _has_changed(self, initial, data):
        """
        Return True if data differs from initial.
        """
        if data is None:
            data_value = b''
        else:
            data_value = data
        if initial is None:
            initial_value = b''
        else:
            initial_value = initial
        if force_text(initial_value) != force_text(data_value):
            return True
        else:
            return False

    def id_for_label(self, id_):
        """
        Returns the HTML ID attribute of this Widget for use by a <label>,
        given the ID of the field. Returns None if no ID is available.

        This hook is necessary because some widgets have multiple HTML
        elements and, thus, multiple IDs. In that case, this method should
        return an ID value that corresponds to the first ID in the widget's
        tags.
        """
        return id_


class Input(Widget):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    input_type = None

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = b''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != b'':
            final_attrs[b'value'] = force_text(self._format_value(value))
        return format_html(b'<input{0} />', flatatt(final_attrs))


class TextInput(Input):
    input_type = b'text'

    def __init__(self, attrs=None):
        if attrs is not None:
            self.input_type = attrs.pop(b'type', self.input_type)
        super(TextInput, self).__init__(attrs)
        return


class PasswordInput(TextInput):
    input_type = b'password'

    def __init__(self, attrs=None, render_value=False):
        super(PasswordInput, self).__init__(attrs)
        self.render_value = render_value

    def render(self, name, value, attrs=None):
        if not self.render_value:
            value = None
        return super(PasswordInput, self).render(name, value, attrs)


class HiddenInput(Input):
    input_type = b'hidden'
    is_hidden = True


class MultipleHiddenInput(HiddenInput):
    """
    A widget that handles <input type="hidden"> for fields that have a list
    of values.
    """

    def __init__(self, attrs=None, choices=()):
        super(MultipleHiddenInput, self).__init__(attrs)
        self.choices = choices

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get(b'id', None)
        inputs = []
        for i, v in enumerate(value):
            input_attrs = dict(value=force_text(v), **final_attrs)
            if id_:
                input_attrs[b'id'] = b'%s_%s' % (id_, i)
            inputs.append(format_html(b'<input{0} />', flatatt(input_attrs)))

        return mark_safe((b'\n').join(inputs))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        else:
            return data.get(name, None)


class FileInput(Input):
    input_type = b'file'
    needs_multipart_form = True

    def render(self, name, value, attrs=None):
        return super(FileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        """File widgets take data from FILES, not POST"""
        return files.get(name, None)

    def _has_changed(self, initial, data):
        if data is None:
            return False
        else:
            return True


FILE_INPUT_CONTRADICTION = object()

class ClearableFileInput(FileInput):
    initial_text = ugettext_lazy(b'Currently')
    input_text = ugettext_lazy(b'Change')
    clear_checkbox_label = ugettext_lazy(b'Clear')
    template_with_initial = b'%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    template_with_clear = b'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the name of the clear checkbox
        input.
        """
        return name + b'-clear'

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input, return the HTML id for it.
        """
        return name + b'_id'

    def render(self, name, value, attrs=None):
        substitutions = {b'initial_text': self.initial_text, 
           b'input_text': self.input_text, 
           b'clear_template': b'', 
           b'clear_checkbox_label': self.clear_checkbox_label}
        template = b'%(input)s'
        substitutions[b'input'] = super(ClearableFileInput, self).render(name, value, attrs)
        if value and hasattr(value, b'url'):
            template = self.template_with_initial
            substitutions[b'initial'] = format_html(b'<a href="{0}">{1}</a>', value.url, force_text(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions[b'clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions[b'clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions[b'clear'] = CheckboxInput().render(checkbox_name, False, attrs={b'id': checkbox_id})
                substitutions[b'clear_template'] = self.template_with_clear % substitutions
        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        upload = super(ClearableFileInput, self).value_from_datadict(data, files, name)
        if not self.is_required and CheckboxInput().value_from_datadict(data, files, self.clear_checkbox_name(name)):
            if upload:
                return FILE_INPUT_CONTRADICTION
            return False
        return upload


class Textarea(Widget):

    def __init__(self, attrs=None):
        default_attrs = {b'cols': b'40', b'rows': b'10'}
        if attrs:
            default_attrs.update(attrs)
        super(Textarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = b''
        final_attrs = self.build_attrs(attrs, name=name)
        return format_html(b'<textarea{0}>\r\n{1}</textarea>', flatatt(final_attrs), force_text(value))


class DateInput(TextInput):

    def __init__(self, attrs=None, format=None):
        super(DateInput, self).__init__(attrs)
        if format:
            self.format = format
            self.manual_format = True
        else:
            self.format = formats.get_format(b'DATE_INPUT_FORMATS')[0]
            self.manual_format = False

    def _format_value(self, value):
        if self.is_localized and not self.manual_format:
            return formats.localize_input(value)
        if hasattr(value, b'strftime'):
            value = datetime_safe.new_date(value)
            return value.strftime(self.format)
        return value

    def _has_changed(self, initial, data):
        try:
            input_format = formats.get_format(b'DATE_INPUT_FORMATS')[0]
            initial = datetime.datetime.strptime(initial, input_format).date()
        except (TypeError, ValueError):
            pass

        return super(DateInput, self)._has_changed(self._format_value(initial), data)


class DateTimeInput(TextInput):

    def __init__(self, attrs=None, format=None):
        super(DateTimeInput, self).__init__(attrs)
        if format:
            self.format = format
            self.manual_format = True
        else:
            self.format = formats.get_format(b'DATETIME_INPUT_FORMATS')[0]
            self.manual_format = False

    def _format_value(self, value):
        if self.is_localized and not self.manual_format:
            return formats.localize_input(value)
        if hasattr(value, b'strftime'):
            value = datetime_safe.new_datetime(value)
            return value.strftime(self.format)
        return value

    def _has_changed(self, initial, data):
        try:
            input_format = formats.get_format(b'DATETIME_INPUT_FORMATS')[0]
            initial = datetime.datetime.strptime(initial, input_format)
        except (TypeError, ValueError):
            pass

        return super(DateTimeInput, self)._has_changed(self._format_value(initial), data)


class TimeInput(TextInput):

    def __init__(self, attrs=None, format=None):
        super(TimeInput, self).__init__(attrs)
        if format:
            self.format = format
            self.manual_format = True
        else:
            self.format = formats.get_format(b'TIME_INPUT_FORMATS')[0]
            self.manual_format = False

    def _format_value(self, value):
        if self.is_localized and not self.manual_format:
            return formats.localize_input(value)
        if hasattr(value, b'strftime'):
            return value.strftime(self.format)
        return value

    def _has_changed(self, initial, data):
        try:
            input_format = formats.get_format(b'TIME_INPUT_FORMATS')[0]
            initial = datetime.datetime.strptime(initial, input_format).time()
        except (TypeError, ValueError):
            pass

        return super(TimeInput, self)._has_changed(self._format_value(initial), data)


def boolean_check(v):
    return not (v is False or v is None or v == b'')


class CheckboxInput(Widget):

    def __init__(self, attrs=None, check_test=None):
        super(CheckboxInput, self).__init__(attrs)
        self.check_test = boolean_check if check_test is None else check_test
        return

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=b'checkbox', name=name)
        if self.check_test(value):
            final_attrs[b'checked'] = b'checked'
        if not (value is True or value is False or value is None or value == b''):
            final_attrs[b'value'] = force_text(value)
        return format_html(b'<input{0} />', flatatt(final_attrs))

    def value_from_datadict(self, data, files, name):
        if name not in data:
            return False
        value = data.get(name)
        values = {b'true': True, b'false': False}
        if isinstance(value, six.string_types):
            value = values.get(value.lower(), value)
        return bool(value)

    def _has_changed(self, initial, data):
        if initial == b'False':
            initial = False
        return bool(initial) != bool(data)


class Select(Widget):
    allow_multiple_selected = False

    def __init__(self, attrs=None, choices=()):
        super(Select, self).__init__(attrs)
        self.choices = list(choices)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = b''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html(b'<select{0}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(b'</select>')
        return mark_safe((b'\n').join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(b' selected="selected"')
            if not self.allow_multiple_selected:
                selected_choices.remove(option_value)
        else:
            selected_html = b''
        return format_html(b'<option value="{0}"{1}>{2}</option>', option_value, selected_html, force_text(option_label))

    def render_options(self, choices, selected_choices):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html(b'<optgroup label="{0}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))

                output.append(b'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))

        return (b'\n').join(output)


class NullBooleanSelect(Select):
    """
    A Select Widget intended to be used with NullBooleanField.
    """

    def __init__(self, attrs=None):
        choices = ((b'1', ugettext_lazy(b'Unknown')),
         (
          b'2', ugettext_lazy(b'Yes')),
         (
          b'3', ugettext_lazy(b'No')))
        super(NullBooleanSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        try:
            value = {True: b'2', False: b'3', b'2': b'2', b'3': b'3'}[value]
        except KeyError:
            value = b'1'

        return super(NullBooleanSelect, self).render(name, value, attrs, choices)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        return {b'2': True, True: True, 
           b'True': True, 
           b'3': False, 
           b'False': False, 
           False: False}.get(value, None)

    def _has_changed(self, initial, data):
        if initial is not None:
            initial = bool(initial)
        if data is not None:
            data = bool(data)
        return initial != data


class SelectMultiple(Select):
    allow_multiple_selected = True

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html(b'<select multiple="multiple"{0}>', flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append(b'</select>')
        return mark_safe((b'\n').join(output))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        else:
            return data.get(name, None)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        else:
            initial_set = set([ force_text(value) for value in initial ])
            data_set = set([ force_text(value) for value in data ])
            return data_set != initial_set


@python_2_unicode_compatible
class RadioInput(SubWidget):
    """
    An object used by RadioFieldRenderer that represents a single
    <input type='radio'>.
    """

    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs
        self.choice_value = force_text(choice[0])
        self.choice_label = force_text(choice[1])
        self.index = index

    def __str__(self):
        return self.render()

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if b'id' in self.attrs:
            label_for = format_html(b' for="{0}_{1}"', self.attrs[b'id'], self.index)
        else:
            label_for = b''
        choice_label = force_text(self.choice_label)
        return format_html(b'<label{0}>{1} {2}</label>', label_for, self.tag(), choice_label)

    def is_checked(self):
        return self.value == self.choice_value

    def tag(self):
        if b'id' in self.attrs:
            self.attrs[b'id'] = b'%s_%s' % (self.attrs[b'id'], self.index)
        final_attrs = dict(self.attrs, type=b'radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs[b'checked'] = b'checked'
        return format_html(b'<input{0} />', flatatt(final_attrs))


@python_2_unicode_compatible
class RadioFieldRenderer(object):
    """
    An object used by RadioSelect to enable customization of radio widgets.
    """

    def __init__(self, name, value, attrs, choices):
        self.name, self.value, self.attrs = name, value, attrs
        self.choices = choices

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield RadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return RadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def __str__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return format_html(b'<ul>\n{0}\n</ul>', format_html_join(b'\n', b'<li>{0}</li>', [ (force_text(w),) for w in self ]))


class RadioSelect(Select):
    renderer = RadioFieldRenderer

    def __init__(self, *args, **kwargs):
        renderer = kwargs.pop(b'renderer', None)
        if renderer:
            self.renderer = renderer
        super(RadioSelect, self).__init__(*args, **kwargs)
        return

    def subwidgets(self, name, value, attrs=None, choices=()):
        for widget in self.get_renderer(name, value, attrs, choices):
            yield widget

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        if value is None:
            value = b''
        str_value = force_text(value)
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        return self.renderer(name, str_value, final_attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        return self.get_renderer(name, value, attrs, choices).render()

    def id_for_label(self, id_):
        if id_:
            id_ += b'_0'
        return id_


class CheckboxSelectMultiple(SelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and b'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [b'<ul>']
        str_values = set([ force_text(v) for v in value ])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            if has_id:
                final_attrs = dict(final_attrs, id=b'%s_%s' % (attrs[b'id'], i))
                label_for = format_html(b' for="{0}"', final_attrs[b'id'])
            else:
                label_for = b''
            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html(b'<li><label{0}>{1} {2}</label></li>', label_for, rendered_cb, option_label))

        output.append(b'</ul>')
        return mark_safe((b'\n').join(output))

    def id_for_label(self, id_):
        if id_:
            id_ += b'_0'
        return id_


class MultiWidget(Widget):
    """
    A widget that is composed of multiple widgets.

    Its render() method is different than other widgets', because it has to
    figure out how to split a single value for display in multiple widgets.
    The ``value`` argument can be one of two things:

        * A list.
        * A normal value (e.g., a string) that has been "compressed" from
          a list of values.

    In the second case -- i.e., if the value is NOT a list -- render() will
    first "decompress" the value into a list before rendering it. It does so by
    calling the decompress() method, which MultiWidget subclasses must
    implement. This method takes a single "compressed" value and returns a
    list.

    When render() does its HTML rendering, each value in the list is rendered
    with the corresponding widget -- the first value is rendered in the first
    widget, the second value is rendered in the second widget, etc.

    Subclasses may implement format_output(), which takes the list of rendered
    widgets and returns a string of HTML that formats them any way you'd like.

    You'll probably want to use this class with MultiValueField.
    """

    def __init__(self, widgets, attrs=None):
        self.widgets = [ isinstance(w, type) and w() or w for w in widgets ]
        super(MultiWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get(b'id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None

            if id_:
                final_attrs = dict(final_attrs, id=b'%s_%s' % (id_, i))
            output.append(widget.render(name + b'_%s' % i, widget_value, final_attrs))

        return mark_safe(self.format_output(output))

    def id_for_label(self, id_):
        if id_:
            id_ += b'_0'
        return id_

    def value_from_datadict(self, data, files, name):
        return [ widget.value_from_datadict(data, files, name + b'_%s' % i) for i, widget in enumerate(self.widgets) ]

    def _has_changed(self, initial, data):
        if initial is None:
            initial = [ b'' for x in range(0, len(data)) ]
        else:
            if not isinstance(initial, list):
                initial = self.decompress(initial)
            for widget, initial, data in zip(self.widgets, initial, data):
                if widget._has_changed(initial, data):
                    return True

        return False

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), returns a Unicode string
        representing the HTML for the whole lot.

        This hook allows you to format the HTML design of the widgets, if
        needed.
        """
        return (b'').join(rendered_widgets)

    def decompress(self, value):
        """
        Returns a list of decompressed values for the given compressed value.
        The given value can be assumed to be valid, but not necessarily
        non-empty.
        """
        raise NotImplementedError(b'Subclasses must implement this method.')

    def _get_media(self):
        """Media for a multiwidget is the combination of all media of the subwidgets"""
        media = Media()
        for w in self.widgets:
            media = media + w.media

        return media

    media = property(_get_media)

    def __deepcopy__(self, memo):
        obj = super(MultiWidget, self).__deepcopy__(memo)
        obj.widgets = copy.deepcopy(self.widgets)
        return obj


class SplitDateTimeWidget(MultiWidget):
    """
    A Widget that splits datetime input into two <input type="text"> boxes.
    """

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (DateInput(attrs=attrs, format=date_format),
         TimeInput(attrs=attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [
             value.date(), value.time().replace(microsecond=0)]
        else:
            return [
             None, None]


class SplitHiddenDateTimeWidget(SplitDateTimeWidget):
    """
    A Widget that splits datetime input into two <input type="hidden"> inputs.
    """
    is_hidden = True

    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(SplitHiddenDateTimeWidget, self).__init__(attrs, date_format, time_format)
        for widget in self.widgets:
            widget.input_type = b'hidden'
            widget.is_hidden = True