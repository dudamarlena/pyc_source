# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/widgets.py
# Compiled at: 2020-02-24 05:12:05
# Size of source mod 2**32: 12263 bytes
"""
Form Widget classes specific to the Django admin site.
"""
from __future__ import absolute_import
from itertools import chain
from django import forms
try:
    from django.forms.widgets import ChoiceWidget as RadioChoiceInput
except:
    from django.forms.widgets import RadioChoiceInput

from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.translation import ugettext as _
from .util import vendor, DJANGO_11

class AdminDateWidget(forms.DateInput):

    @property
    def media(self):
        return vendor('datepicker.js', 'datepicker.css', 'xadmin.widget.datetime.js')

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class':'date-field form-control', 
         'size':'10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminDateWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None, **kwargs):
        input_html = (super(AdminDateWidget, self).render)(name, value, attrs=attrs, **kwargs)
        return mark_safe('<div class="input-group date bootstrap-datepicker"><span class="input-group-addon"><i class="fa fa-calendar"></i></span>%s<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>' % (
         input_html, _('Today')))


class AdminTimeWidget(forms.TimeInput):

    @property
    def media(self):
        return vendor('datepicker.js', 'clockpicker.js', 'clockpicker.css', 'xadmin.widget.datetime.js')

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class':'time-field form-control', 
         'size':'8'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTimeWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None, **kwargs):
        input_html = (super(AdminTimeWidget, self).render)(name, value, attrs=attrs, **kwargs)
        return mark_safe('<div class="input-group time bootstrap-clockpicker"><span class="input-group-addon"><i class="fa fa-clock-o"></i></span>%s<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>' % (
         input_html, _('Now')))


class AdminSelectWidget(forms.Select):

    def render(self, name, value, attrs=None, **kwargs):
        attrs['class'] = attrs.get('class', '') + 'select form-control'
        return (super(AdminSelectWidget, self).render)(name, value, attrs=attrs, **kwargs)

    @property
    def media(self):
        return vendor('select.js', 'select.css', 'xadmin.widget.select.js')


class AdminSplitDateTime(forms.SplitDateTimeWidget):
    __doc__ = '\n    A SplitDateTime Widget that has some admin-specific styling.\n    '

    def __init__(self, attrs=None):
        widgets = [
         AdminDateWidget, AdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def render(self, name, value, attrs=None, **kwargs):
        if DJANGO_11:
            input_html = [ht for ht in (super(AdminSplitDateTime, self).render)(name, value, attrs=attrs, **kwargs).replace('><input', '>\n<input').split('\n') if ht != '']
            return mark_safe('<div class="datetime clearfix"><div class="input-group date bootstrap-datepicker"><span class="input-group-addon"><i class="fa fa-calendar"></i></span>%s<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div><div class="input-group time bootstrap-clockpicker"><span class="input-group-addon"><i class="fa fa-clock-o"></i></span>%s<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div></div>' % (
             input_html[0], _('Today'), input_html[1], _('Now')))
        else:
            return (super(AdminSplitDateTime, self).render)(name, value, attrs=attrs, **kwargs)

    def format_output(self, rendered_widgets):
        return mark_safe('<div class="datetime clearfix">%s%s</div>' % (
         rendered_widgets[0], rendered_widgets[1]))


class AdminRadioInput(forms.CheckboxInput):
    input_type = 'radio'

    def format_value(self, value):
        """Only return the 'value' attribute if value isn't None or boolean."""
        if value is True or value is False or value is None:
            return
        else:
            return force_text(value)


class AdminRadioSelect(RadioChoiceInput):

    def render(self, name, value, attrs=None, choices=(), **kwargs):
        if value is None:
            value = []
        else:
            if type(value) not in (list, tuple):
                value = [value]
            else:
                if attrs:
                    attrs.update(self.attrs)
                else:
                    attrs = self.attrs
            attrs['class'] = attrs.get('class', '').replace('form-control', '')
            if DJANGO_11:
                final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})
            else:
                final_attrs = self.build_attrs(attrs, name=name)
        output = []
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            radio_input = AdminRadioInput(final_attrs, check_test=(lambda value: value in str_values))
            option_value = force_text(option_value)
            rendered_radio_input = radio_input.render(name, option_value)
            option_label = conditional_escape(force_text(option_label))
            if final_attrs.get('inline', False):
                output.append('<label class="radio-inline">%s %s</label>' % (rendered_radio_input, option_label))
            else:
                output.append('<div class="radio"><label>%s %s</label></div>' % (rendered_radio_input, option_label))

        return mark_safe('\n'.join(output))


class AdminCheckboxSelect(RadioChoiceInput):
    allow_multiple_selected = True
    input_type = 'checkbox'

    def __init__(self, attrs=None, can_add_related=True):
        self.can_add_related = can_add_related
        super(AdminCheckboxSelect, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None, choices=(), **kwargs):
        if value is None:
            value = []
        else:
            if attrs:
                attrs.update(self.attrs)
            else:
                attrs = self.attrs
            attrs['class'] = attrs.get('class', '').replace('form-control', '')
            has_id = attrs and 'id' in attrs
            if DJANGO_11:
                final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})
            else:
                final_attrs = self.build_attrs(attrs, name=name)
        output = []
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            if has_id:
                final_attrs = dict(final_attrs, id=('%s_%s' % (attrs['id'], i)))
                label_for = ' for="%s"' % final_attrs['id']
            else:
                label_for = ''
            cb = forms.CheckboxInput(final_attrs,
              check_test=(lambda value: value in str_values))
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_text(option_label))
            if final_attrs.get('inline', False):
                output.append('<label%s class="checkbox-inline">%s %s</label>' % (label_for, rendered_cb, option_label))
            else:
                output.append('<div class="checkbox"><label%s>%s %s</label></div>' % (label_for, rendered_cb, option_label))

        return mark_safe('\n'.join(output))


class AdminSelectMultiple(forms.SelectMultiple):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'select-multi'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminSelectMultiple, self).__init__(attrs=final_attrs)


class AdminFileWidget(forms.ClearableFileInput):
    template_with_initial = '<p class="file-upload">%s</p>' % forms.ClearableFileInput.initial_text
    template_with_clear = '<span class="clearable-file-input">%s</span>' % forms.ClearableFileInput.clear_checkbox_label


class AdminTextareaWidget(forms.Textarea):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'textarea-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTextareaWidget, self).__init__(attrs=final_attrs)


class AdminTextInputWidget(forms.TextInput):
    template_name = 'xadmin/widgets/text.html'

    def __init__(self, attrs=None):
        final_attrs = {'class': 'text-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTextInputWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None, **kwargs):
        if self.attrs.get('readonly'):
            if self.attrs.get('class'):
                self.attrs['class'] = self.attrs['class'].replace('form-control', 'form-control-static')
                self.attrs['style'] = 'border-width: 0px;'
        return (super(AdminTextInputWidget, self).render)(name, value, attrs=attrs, **kwargs)


class AdminURLFieldWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'url-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminURLFieldWidget, self).__init__(attrs=final_attrs)


class AdminIntegerFieldWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'int-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminIntegerFieldWidget, self).__init__(attrs=final_attrs)


class AdminCommaSeparatedIntegerFieldWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'sep-int-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminCommaSeparatedIntegerFieldWidget, self).__init__(attrs=final_attrs)