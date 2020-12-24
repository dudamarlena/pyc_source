# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/forms/fields.py
# Compiled at: 2010-02-24 11:41:18
try:
    from django import newforms as forms
    from django.newforms import fields
except:
    from django import forms
    from django.forms import fields

from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from softwarefabrica.django.forms.widgets import *
reverse_lazy = lazy(reverse, unicode)

class NullBooleanField(fields.NullBooleanField):
    """
    A field whose valid values are None, True and False. Invalid values are
    cleaned to None.

    This avoids Django bug #9473:
    http://code.djangoproject.com/ticket/9473
    """
    __module__ = __name__
    widget = NullBooleanSelect


class DateTimeField(forms.DateTimeField):
    """
    A replacement for django.forms.DateTimeField which uses a nice
    popup JavaScript calendar for date/time selection.
    """
    __module__ = __name__
    widget = DateTimeWidget

    def __init__(self, *args, **kwargs):
        input_formats = kwargs.get('input_formats', fields.DEFAULT_DATETIME_INPUT_FORMATS)
        self.widget.input_formats = input_formats
        super(DateTimeField, self).__init__(*args, **kwargs)


class DateField(forms.DateField):
    """
    A replacement for django.forms.DateField which uses a nice
    popup JavaScript calendar for date selection.
    """
    __module__ = __name__
    widget = DateWidget

    def __init__(self, *args, **kwargs):
        input_formats = kwargs.get('input_formats', fields.DEFAULT_DATE_INPUT_FORMATS)
        self.widget.input_formats = input_formats
        super(DateField, self).__init__(*args, **kwargs)


try:
    from django.newforms.util import ErrorList, ValidationError
    from django.newforms.fields import EMPTY_VALUES
except:
    from django.forms.util import ErrorList, ValidationError
    from django.forms.fields import EMPTY_VALUES

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import StrAndUnicode, smart_unicode, smart_str

class DateRangeField(fields.Field):
    """
    A form field for selecting date ranges with a nice
    popup JavaScript calendar.
    """
    __module__ = __name__
    widget = DateRangeWidget
    default_error_messages = {'invalid': _('Enter a valid date range.')}

    def __init__(self, *args, **kwargs):
        input_formats = kwargs.pop('input_formats', fields.DEFAULT_DATE_INPUT_FORMATS)
        self.input_formats = input_formats
        self.widget.input_formats = input_formats
        super(DateRangeField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Validates that the input can be converted to a datetime or datetime pair.
        Returns a Python datetime.datetime object or pair.
        """
        super(DateRangeField, self).clean(value)
        if value in EMPTY_VALUES:
            return
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        if isinstance(value, list):
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid'])
            (date1, date2) = (None, None)
            (date1_v, date2_v) = value
            if type(date1_v) == type('') or type(date1_v) == type('') and date1_v and date1_v != '':
                date1 = datetime.datetime(*time.strptime(date1_v, '%d/%m/%Y')[:3])
            if type(date2_v) == type('') or type(date2_v) == type('') and date2_v and date2_v != '':
                date2 = datetime.datetime(*time.strptime(date2_v, '%d/%m/%Y')[:3])
            value = (date1, date2)
            return value
        try:
            date1 = None
            date2 = None
            m = date_range_re.match(value)
            if m:
                (date1_s, date2_s) = m.groups()
                if date1_s and date1_s != '':
                    date1 = datetime.datetime(*time.strptime(date1_s, '%d/%m/%Y')[:3])
                if date2_s and date2_s != '':
                    date2 = datetime.datetime(*time.strptime(date2_s, '%d/%m/%Y')[:3])
            return (
             date1, date2)
        except ValueError:
            raise ValidationError(self.error_messages['invalid'])

        return


class RelatedItemField(forms.ModelChoiceField):
    """
    A field for softwarefabrica.django.forms.widgets.RelatedItemWidget

    This is a field that allows the selection of an object
    (model instance) from a QuerySet using a popup interface.

    This derives from (new)forms.ModelChoiceField but using the
    RelatedItemWidget to allow selecting with a popup interface.
    """
    __module__ = __name__
    widget = RelatedItemWidget

    def __init__(self, queryset, empty_label='---------', cache_choices=False, required=False, widget=RelatedItemWidget, label=None, initial=None, help_text=None, *args, **kwargs):
        if not (hasattr(queryset.model, 'get_list_url') or hasattr(queryset.model, 'get_create_url')):
            widget = forms.Select
        super(RelatedItemField, self).__init__(queryset, empty_label, cache_choices, required, widget, label, initial, help_text, *args, **kwargs)
        self.widget.model = queryset.model


class SelectPopupField(forms.ModelChoiceField):
    """
    A field for softwarefabrica.django.forms.widgets.SelectPopupWidget

    This is a field that allows the selection of an object
    (model instance) from a QuerySet using a popup interface.

    This derives from (new)forms.ModelChoiceField but using the
    SelectPopupWidget to allow selecting with a popup interface.
    """
    __module__ = __name__
    widget = SelectPopupWidget

    def __init__(self, queryset, empty_label='---------', cache_choices=False, required=False, widget=SelectPopupWidget, label=None, initial=None, help_text=None, *args, **kwargs):
        if not (hasattr(queryset.model, 'get_list_url') or hasattr(queryset.model, 'get_edit_url') or hasattr(queryset.model, 'get_create_url')):
            widget = forms.Select
        else:
            from django.db.models.query import QuerySet
            assert isinstance(queryset, QuerySet)
            if widget == SelectPopupWidget:
                widget = SelectPopupWidget(model=queryset.model)
        super(SelectPopupField, self).__init__(queryset, empty_label, cache_choices, required, widget, label, initial, help_text, *args, **kwargs)
        self.widget.model = queryset.model


class SelectMultiplePopupField(forms.ModelMultipleChoiceField):
    """
    A field for softwarefabrica.django.forms.widgets.SelectMultiplePopupWidget

    This is a field that allows the selection of a set of objects
    (model instances) from a QuerySet using a popup interface.

    This derives from (new)forms.ModelMultipleChoiceField but using the
    SelectMultiplePopupWidget to allow selecting with a popup interface.
    """
    __module__ = __name__
    widget = SelectMultiplePopupWidget

    def __init__(self, queryset, cache_choices=False, required=False, widget=SelectMultiplePopupWidget, label=None, initial=None, help_text=None, empty_label='---------', *args, **kwargs):
        if not (hasattr(queryset.model, 'get_list_url') or hasattr(queryset.model, 'get_edit_url') or hasattr(queryset.model, 'get_create_url')):
            widget = forms.SelectMultiple
        else:
            from django.db.models.query import QuerySet
            assert isinstance(queryset, QuerySet)
            if widget == SelectMultiplePopupWidget:
                widget = SelectMultiplePopupWidget(model=queryset.model)
        super(SelectMultiplePopupField, self).__init__(queryset, cache_choices, required, widget, label, initial, help_text, *args, **kwargs)
        self.widget.model = queryset.model


ModelChoiceField = SelectPopupField
ModelMultipleChoiceField = SelectMultiplePopupField

class SelectCascadeField(forms.ModelChoiceField):
    """
    A field for softwarefabrica.django.forms.widgets.SelectCascadeWidget

    This is a field that allows the selection of an object
    (model instance) from a QuerySet using a popup interface.

    This derives from (new)forms.ModelChoiceField but using the
    SelectPopupWidget to allow selecting with a popup interface.

    See the companion softwarefabrica.django.forms.widgets.SelectCascadeWidget
    form widget.

    The constructor requires:
      - the 'slave_model' for the cascaded slave select;
      - the 'slave_pivot_field', which is the field in the slave model which
        references the master 'model';
      - [OPTIONAL] the 'cascade_url' for the AJAX selection/filtering view.
    """
    __module__ = __name__
    widget = SelectCascadeWidget

    def __init__(self, queryset, slave_model, slave_pivot_field, empty_label='---------', cache_choices=False, required=False, widget=SelectCascadeWidget, label=None, initial=None, help_text=None, *args, **kwargs):
        from django.db.models.query import QuerySet
        assert isinstance(queryset, QuerySet)
        master_selector = kwargs.pop('master_selector', None)
        slave_selector = kwargs.pop('slave_selector', None)
        slave_widget = kwargs.pop('slave_widget', None)
        cascade_url = kwargs.pop('cascade_url', None)
        if widget == SelectCascadeWidget:
            widget = SelectCascadeWidget(model=queryset.model, slave_model=slave_model, slave_pivot_field=slave_pivot_field, cascade_url=cascade_url, master_selector=master_selector, slave_selector=slave_selector, slave_widget=slave_widget)
        super(SelectCascadeField, self).__init__(queryset, empty_label, cache_choices, required, widget, label, initial, help_text, *args, **kwargs)
        self.widget.model = queryset.model
        return


class SelectCascadePopupField(SelectPopupField):
    """
    A field for softwarefabrica.django.forms.widgets.SelectCascadePopupWidget

    This is an extended field that allows the selection of an object
    (model instance) from a QuerySet using a popup interface.
    This extension allows the cascaded update of a slave
    (ForeignKey) Select field through AJAX.

    This derives from SelectPopupField but using the
    SelectCascadePopupWidget to allow the cascaded
    update of the slave Select widget through AJAX.

    See the companion softwarefabrica.django.forms.widgets.SelectCascadePopupWidget
    form widget.

    The constructor requires:
      - the 'slave_model' for the cascaded slave select;
      - the 'slave_pivot_field', which is the field in the slave model which
        references the master 'model';
      - [OPTIONAL] the 'cascade_url' for the AJAX selection/filtering view.
    """
    __module__ = __name__
    widget = SelectCascadePopupWidget

    def __init__(self, queryset, slave_model, slave_pivot_field, empty_label='---------', cache_choices=False, required=False, widget=SelectCascadeWidget, label=None, initial=None, help_text=None, *args, **kwargs):
        if not (hasattr(queryset.model, 'get_list_url') or hasattr(queryset.model, 'get_edit_url') or hasattr(queryset.model, 'get_create_url')):
            widget = forms.Select
        else:
            from django.db.models.query import QuerySet
            assert isinstance(queryset, QuerySet)
            master_selector = kwargs.pop('master_selector', None)
            slave_selector = kwargs.pop('slave_selector', None)
            slave_widget = kwargs.pop('slave_widget', None)
            cascade_url = kwargs.pop('cascade_url', None)
            if widget == SelectCascadePopupWidget:
                widget = SelectCascadePopupWidget(model=queryset.model, slave_model=slave_model, slave_pivot_field=slave_pivot_field, cascade_url=cascade_url, master_selector=master_selector, slave_selector=slave_selector, slave_widget=slave_widget)
        super(SelectCascadePopupField, self).__init__(queryset, empty_label, cache_choices, required, widget, label, initial, help_text, *args, **kwargs)
        self.widget.model = queryset.model
        return