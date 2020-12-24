# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller/renderers.py
# Compiled at: 2017-02-17 14:40:23
from __future__ import unicode_literals
try:
    from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
except RuntimeError:
    ReadOnlyPasswordHashWidget = None

from django.forms import TextInput, DateInput, FileInput, CheckboxInput, MultiWidget, ClearableFileInput, Select, RadioSelect, CheckboxSelectMultiple
from django.forms.extras import SelectDateWidget
from django.forms.forms import BaseForm, BoundField
from django.forms.formsets import BaseFormSet
from django.utils.html import conditional_escape, escape, strip_tags
from django.utils.safestring import mark_safe
from .propeller import get_propeller_setting, PROPELLER_SET_REQUIRED_SET_DISABLED
from .exceptions import PropellerError
from .forms import render_form, render_field, render_label, render_form_group, is_widget_with_placeholder, FORM_GROUP_CLASS, is_widget_required_attribute
from .text import text_value
from .utils import add_css_class, render_template_file

class BaseRenderer(object):
    """
    A content renderer
    """

    def __init__(self, *args, **kwargs):
        self.layout = kwargs.get(b'layout', b'')
        self.form_group_class = kwargs.get(b'form_group_class', FORM_GROUP_CLASS)
        self.field_class = kwargs.get(b'field_class', b'')
        self.label_class = kwargs.get(b'label_class', b'')
        self.show_help = kwargs.get(b'show_help', True)
        self.show_label = kwargs.get(b'show_label', True)
        self.exclude = kwargs.get(b'exclude', b'')
        self.set_required = kwargs.get(b'set_required', True)
        self.set_disabled = kwargs.get(b'set_disabled', False)
        self.set_placeholder = kwargs.get(b'set_placeholder', True)
        self.size = self.parse_size(kwargs.get(b'size', b''))
        self.horizontal_label_class = kwargs.get(b'horizontal_label_class', get_propeller_setting(b'horizontal_label_class'))
        self.horizontal_field_class = kwargs.get(b'horizontal_field_class', get_propeller_setting(b'horizontal_field_class'))

    @staticmethod
    def parse_size(size):
        size = text_value(size).lower().strip()
        if size in ('sm', 'small'):
            return b'small'
        if size in ('lg', 'large'):
            return b'large'
        if size in ('md', 'medium', ''):
            return b'medium'
        raise PropellerError(b'Invalid value "%s" for parameter "size" (expected "sm", "md", "lg" or "").' % size)

    def get_size_class(self, prefix=b'input'):
        if self.size == b'small':
            return prefix + b'-sm'
        if self.size == b'large':
            return prefix + b'-lg'
        return b''

    def _render(self):
        return b''

    def render(self):
        return mark_safe(self._render())


class FormsetRenderer(BaseRenderer):
    """
    Default formset renderer
    """

    def __init__(self, formset, *args, **kwargs):
        if not isinstance(formset, BaseFormSet):
            raise PropellerError(b'Parameter "formset" should contain a valid Django Formset.')
        self.formset = formset
        super(FormsetRenderer, self).__init__(*args, **kwargs)

    def render_management_form(self):
        return text_value(self.formset.management_form)

    @staticmethod
    def render_form(form, **kwargs):
        return render_form(form, **kwargs)

    def render_forms(self):
        rendered_forms = []
        for form in self.formset.forms:
            rendered_forms.append(self.render_form(form, layout=self.layout, form_group_class=self.form_group_class, field_class=self.field_class, label_class=self.label_class, show_label=self.show_label, show_help=self.show_help, exclude=self.exclude, set_required=self.set_required, set_disabled=self.set_disabled, set_placeholder=self.set_placeholder, size=self.size, horizontal_label_class=self.horizontal_label_class, horizontal_field_class=self.horizontal_field_class))

        return (b'\n').join(rendered_forms)

    def get_formset_errors(self):
        return self.formset.non_form_errors()

    def render_errors(self):
        formset_errors = self.get_formset_errors()
        if formset_errors:
            return render_template_file(b'propeller/form_errors.html', context={b'errors': formset_errors, 
               b'form': self.formset, 
               b'layout': self.layout})
        return b''

    def _render(self):
        return (b'{}{}{}').format(self.render_errors(), self.render_management_form(), self.render_forms())


class FormRenderer(BaseRenderer):
    """
    Default form renderer
    """

    def __init__(self, form, *args, **kwargs):
        if not isinstance(form, BaseForm):
            raise PropellerError(b'Parameter "form" should contain a valid Django Form.')
        self.form = form
        super(FormRenderer, self).__init__(*args, **kwargs)
        if PROPELLER_SET_REQUIRED_SET_DISABLED and self.form.empty_permitted:
            self.set_required = False
        self.error_css_class = kwargs.get(b'error_css_class', None)
        self.required_css_class = kwargs.get(b'required_css_class', None)
        self.bound_css_class = kwargs.get(b'bound_css_class', None)
        return

    def render_fields(self):
        rendered_fields = []
        for field in self.form:
            rendered_fields.append(render_field(field, layout=self.layout, form_group_class=self.form_group_class, field_class=self.field_class, label_class=self.label_class, show_label=self.show_label, show_help=self.show_help, exclude=self.exclude, set_required=self.set_required, set_disabled=self.set_disabled, set_placeholder=self.set_placeholder, size=self.size, horizontal_label_class=self.horizontal_label_class, horizontal_field_class=self.horizontal_field_class, error_css_class=self.error_css_class, required_css_class=self.required_css_class, bound_css_class=self.bound_css_class))

        return (b'\n').join(rendered_fields)

    def get_fields_errors(self):
        form_errors = []
        for field in self.form:
            if not field.is_hidden and field.errors:
                form_errors += field.errors

        return form_errors

    def render_errors(self, _type=b'all'):
        form_errors = None
        if _type == b'all':
            form_errors = self.get_fields_errors() + self.form.non_field_errors()
        elif _type == b'fields':
            form_errors = self.get_fields_errors()
        elif _type == b'non_fields':
            form_errors = self.form.non_field_errors()
        if form_errors:
            return render_template_file(b'propeller/form_errors.html', context={b'errors': form_errors, 
               b'form': self.form, 
               b'layout': self.layout, 
               b'type': _type})
        else:
            return b''

    def _render(self):
        return self.render_errors() + self.render_fields()


class FieldRenderer(BaseRenderer):
    """
    Default field renderer
    """
    WIDGETS_NO_FORM_CONTROL = (
     CheckboxInput,
     RadioSelect,
     CheckboxSelectMultiple,
     FileInput)

    def __init__(self, field, *args, **kwargs):
        if not isinstance(field, BoundField):
            raise PropellerError(b'Parameter "field" should contain a valid Django BoundField.')
        self.field = field
        super(FieldRenderer, self).__init__(*args, **kwargs)
        self.widget = field.field.widget
        self.is_multi_widget = isinstance(field.field.widget, MultiWidget)
        self.initial_attrs = self.widget.attrs.copy()
        self.field_help = text_value(mark_safe(field.help_text)) if self.show_help and field.help_text else b''
        self.field_errors = [ conditional_escape(text_value(error)) for error in field.errors ]
        if b'placeholder' in kwargs:
            self.placeholder = kwargs[b'placeholder']
        elif get_propeller_setting(b'set_placeholder'):
            self.placeholder = field.label
        else:
            self.placeholder = b''
        self.addon_before = kwargs.get(b'addon_before', self.widget.attrs.pop(b'addon_before', b''))
        self.addon_after = kwargs.get(b'addon_after', self.widget.attrs.pop(b'addon_after', b''))
        self.addon_before_class = kwargs.get(b'addon_before_class', self.widget.attrs.pop(b'addon_before_class', b'input-group-addon'))
        self.addon_after_class = kwargs.get(b'addon_after_class', self.widget.attrs.pop(b'addon_after_class', b'input-group-addon'))
        error_css_class = kwargs.get(b'error_css_class', None)
        required_css_class = kwargs.get(b'required_css_class', None)
        bound_css_class = kwargs.get(b'bound_css_class', None)
        if error_css_class is not None:
            self.error_css_class = error_css_class
        else:
            self.error_css_class = getattr(field.form, b'error_css_class', get_propeller_setting(b'error_css_class'))
        if required_css_class is not None:
            self.required_css_class = required_css_class
        else:
            self.required_css_class = getattr(field.form, b'required_css_class', get_propeller_setting(b'required_css_class'))
        if bound_css_class is not None:
            self.success_css_class = bound_css_class
        else:
            self.success_css_class = getattr(field.form, b'bound_css_class', get_propeller_setting(b'success_css_class'))
        if self.field.form.empty_permitted:
            self.required_css_class = b''
        if PROPELLER_SET_REQUIRED_SET_DISABLED:
            if self.field.form.empty_permitted:
                self.set_required = False
            self.set_disabled = kwargs.get(b'set_disabled', False)
        return

    def restore_widget_attrs(self):
        self.widget.attrs = self.initial_attrs.copy()

    def add_class_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        classes = widget.attrs.get(b'class', b'')
        if ReadOnlyPasswordHashWidget is not None and isinstance(widget, ReadOnlyPasswordHashWidget):
            classes = add_css_class(classes, b'form-control-static', prepend=True)
        elif not isinstance(widget, self.WIDGETS_NO_FORM_CONTROL):
            classes = add_css_class(classes, b'form-control', prepend=True)
            classes = add_css_class(classes, self.get_size_class())
        widget.attrs[b'class'] = classes
        return

    def add_placeholder_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        placeholder = widget.attrs.get(b'placeholder', self.placeholder)
        if placeholder and self.set_placeholder and is_widget_with_placeholder(widget):
            widget.attrs[b'placeholder'] = placeholder
        return

    def add_help_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        if not isinstance(widget, CheckboxInput):
            widget.attrs[b'title'] = widget.attrs.get(b'title', escape(strip_tags(self.field_help)))
        return

    def add_required_attrs(self, widget=None):
        """
        Only relevant if DBS3_SET_REQUIRED_SET_DISABLED
        """
        if widget is None:
            widget = self.widget
        if self.set_required and is_widget_required_attribute(widget):
            widget.attrs[b'required'] = b'required'
        return

    def add_disabled_attrs(self, widget=None):
        """
        Only relevant if DBS3_SET_REQUIRED_SET_DISABLED
        """
        if widget is None:
            widget = self.widget
        if self.set_disabled:
            widget.attrs[b'disabled'] = b'disabled'
        return

    def add_widget_attrs(self):
        if self.is_multi_widget:
            widgets = self.widget.widgets
        else:
            widgets = [
             self.widget]
        for widget in widgets:
            self.add_class_attrs(widget)
            self.add_placeholder_attrs(widget)
            self.add_help_attrs(widget)
            if PROPELLER_SET_REQUIRED_SET_DISABLED:
                self.add_required_attrs(widget)
                self.add_disabled_attrs(widget)

    def list_to_class(self, html, klass):
        classes = add_css_class(klass, self.get_size_class())
        mapping = [
         ('<ul', '<div'),
         ('</ul>', '</div>'),
         (
          b'<li', (b'<div class="{klass}"').format(klass=classes)),
         ('</li>', '</div>')]
        for k, v in mapping:
            html = html.replace(k, v)

        return html

    def put_inside_label(self, html):
        content = (b'{field} {label}').format(field=html, label=self.field.label)
        return render_label(content=mark_safe(content), label_for=self.field.id_for_label, label_title=escape(strip_tags(self.field_help)))

    @staticmethod
    def fix_date_select_input(html):
        div1 = b'<div class="col-xs-4">'
        div2 = b'</div>'
        html = html.replace(b'<select', div1 + b'<select')
        html = html.replace(b'</select>', b'</select>' + div2)
        return b'<div class="row bootstrap3-multi-input">' + html + b'</div>'

    @staticmethod
    def fix_clearable_file_input(html):
        """
        Fix a clearable file input
        TODO: This needs improvement

        Currently Django returns
        Currently:
        <a href="dummy.txt">dummy.txt</a>
        <input id="file4-clear_id" name="file4-clear" type="checkbox" />
        <label for="file4-clear_id">Clear</label><br />
        Change: <input id="id_file4" name="file4" type="file" />
        <span class=help-block></span>
        </div>

        """
        return (b'<div class="row bootstrap3-multi-input"><div class="col-xs-12">{html}</div></div>').format(html=html)

    def post_widget_render(self, html):
        if isinstance(self.widget, RadioSelect):
            html = self.list_to_class(html, b'radio')
        elif isinstance(self.widget, CheckboxSelectMultiple):
            html = self.list_to_class(html, b'checkbox')
        elif isinstance(self.widget, SelectDateWidget):
            html = self.fix_date_select_input(html)
        elif isinstance(self.widget, ClearableFileInput):
            html = self.fix_clearable_file_input(html)
        elif isinstance(self.widget, CheckboxInput):
            html = self.put_inside_label(html)
        return html

    def wrap_widget(self, html):
        if isinstance(self.widget, CheckboxInput):
            html = (b'<div class="checkbox">{content}</div>').format(content=html)
        return html

    def make_input_group(self, html):
        if (self.addon_before or self.addon_after) and isinstance(self.widget, (TextInput, DateInput, Select)):
            before = (b'<span class="{input_class}">{addon}</span>').format(input_class=self.addon_before_class, addon=self.addon_before) if self.addon_before else b''
            after = (b'<span class="{input_class}">{addon}</span>').format(input_class=self.addon_after_class, addon=self.addon_after) if self.addon_after else b''
            html = (b'<div class="input-group">{before}{html}{after}</div>').format(before=before, after=after, html=html)
        return html

    def append_to_field(self, html):
        help_text_and_errors = []
        if self.field_help:
            help_text_and_errors.append(self.field_help)
        help_text_and_errors += self.field_errors
        if help_text_and_errors:
            help_html = render_template_file(b'propeller/field_help_text_and_errors.html', context={b'field': self.field, 
               b'help_text_and_errors': help_text_and_errors, 
               b'layout': self.layout, 
               b'show_help': self.show_help})
            html += (b'<span class="help-block">{help}</span>').format(help=help_html)
        return html

    def get_field_class(self):
        field_class = self.field_class
        if not field_class and self.layout == b'horizontal':
            field_class = self.horizontal_field_class
        return field_class

    def wrap_field(self, html):
        field_class = self.get_field_class()
        if field_class:
            html = (b'<div class="{klass}">{html}</div>').format(klass=field_class, html=html)
        return html

    def get_label_class(self):
        label_class = self.label_class
        if not label_class and self.layout == b'horizontal':
            label_class = self.horizontal_label_class
        label_class = text_value(label_class)
        if not self.show_label:
            label_class = add_css_class(label_class, b'sr-only')
        return add_css_class(label_class, b'control-label')

    def get_label(self):
        if isinstance(self.widget, CheckboxInput):
            label = None
        else:
            label = self.field.label
        if self.layout == b'horizontal' and not label:
            return mark_safe(b'&#160;')
        else:
            return label

    def add_label(self, html):
        label = self.get_label()
        if label:
            html = render_label(label, label_for=self.field.id_for_label, label_class=self.get_label_class()) + html
        return html

    def get_form_group_class(self):
        form_group_class = self.form_group_class
        if self.field.errors:
            if self.error_css_class:
                form_group_class = add_css_class(form_group_class, self.error_css_class)
        elif self.field.form.is_bound:
            form_group_class = add_css_class(form_group_class, self.success_css_class)
        if self.field.field.required and self.required_css_class:
            form_group_class = add_css_class(form_group_class, self.required_css_class)
        if self.layout == b'horizontal':
            form_group_class = add_css_class(form_group_class, self.get_size_class(prefix=b'form-group'))
        return form_group_class

    def wrap_label_and_field(self, html):
        return render_form_group(html, self.get_form_group_class())

    def _render(self):
        if self.field.name in self.exclude.replace(b' ', b'').split(b','):
            return b''
        if self.field.is_hidden:
            return text_value(self.field)
        self.add_widget_attrs()
        html = self.field.as_widget(attrs=self.widget.attrs)
        self.restore_widget_attrs()
        html = self.post_widget_render(html)
        html = self.wrap_widget(html)
        html = self.make_input_group(html)
        html = self.append_to_field(html)
        html = self.wrap_field(html)
        html = self.add_label(html)
        html = self.wrap_label_and_field(html)
        return html


class InlineFieldRenderer(FieldRenderer):
    """
    Inline field renderer
    """

    def add_error_attrs(self):
        field_title = self.widget.attrs.get(b'title', b'')
        field_title += b' ' + (b' ').join([ strip_tags(e) for e in self.field_errors ])
        self.widget.attrs[b'title'] = field_title.strip()

    def add_widget_attrs(self):
        super(InlineFieldRenderer, self).add_widget_attrs()
        self.add_error_attrs()

    def append_to_field(self, html):
        return html

    def get_field_class(self):
        return self.field_class

    def get_label_class(self):
        return add_css_class(self.label_class, b'sr-only')