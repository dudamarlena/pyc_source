# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/forms/formsets.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.forms.widgets import HiddenInput
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.html import html_safe
from django.utils.safestring import mark_safe
from django.utils.six.moves import range
from django.utils.translation import ugettext as _, ungettext
__all__ = (
 b'BaseFormSet', b'formset_factory', b'all_valid')
TOTAL_FORM_COUNT = b'TOTAL_FORMS'
INITIAL_FORM_COUNT = b'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = b'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = b'MAX_NUM_FORMS'
ORDERING_FIELD_NAME = b'ORDER'
DELETION_FIELD_NAME = b'DELETE'
DEFAULT_MIN_NUM = 0
DEFAULT_MAX_NUM = 1000

class ManagementForm(Form):
    """
    ``ManagementForm`` is used to keep track of how many form instances
    are displayed on the page. If adding new forms via javascript, you should
    increment the count field of this form as well.
    """

    def __init__(self, *args, **kwargs):
        self.base_fields[TOTAL_FORM_COUNT] = IntegerField(widget=HiddenInput)
        self.base_fields[INITIAL_FORM_COUNT] = IntegerField(widget=HiddenInput)
        self.base_fields[MIN_NUM_FORM_COUNT] = IntegerField(required=False, widget=HiddenInput)
        self.base_fields[MAX_NUM_FORM_COUNT] = IntegerField(required=False, widget=HiddenInput)
        super(ManagementForm, self).__init__(*args, **kwargs)


@html_safe
@python_2_unicode_compatible
class BaseFormSet(object):
    """
    A collection of instances of the same Form class.
    """

    def __init__(self, data=None, files=None, auto_id=b'id_%s', prefix=None, initial=None, error_class=ErrorList, form_kwargs=None):
        self.is_bound = data is not None or files is not None
        self.prefix = prefix or self.get_default_prefix()
        self.auto_id = auto_id
        self.data = data or {}
        self.files = files or {}
        self.initial = initial
        self.form_kwargs = form_kwargs or {}
        self.error_class = error_class
        self._errors = None
        self._non_form_errors = None
        return

    def __str__(self):
        return self.as_table()

    def __iter__(self):
        """Yields the forms in the order they should be rendered"""
        return iter(self.forms)

    def __getitem__(self, index):
        """Returns the form at the given index, based on the rendering order"""
        return self.forms[index]

    def __len__(self):
        return len(self.forms)

    def __bool__(self):
        """All formsets have a management form which is not included in the length"""
        return True

    def __nonzero__(self):
        return type(self).__bool__(self)

    @cached_property
    def management_form(self):
        """Returns the ManagementForm instance for this FormSet."""
        if self.is_bound:
            form = ManagementForm(self.data, auto_id=self.auto_id, prefix=self.prefix)
            if not form.is_valid():
                raise ValidationError(_(b'ManagementForm data is missing or has been tampered with'), code=b'missing_management_form')
        else:
            form = ManagementForm(auto_id=self.auto_id, prefix=self.prefix, initial={TOTAL_FORM_COUNT: self.total_form_count(), 
               INITIAL_FORM_COUNT: self.initial_form_count(), 
               MIN_NUM_FORM_COUNT: self.min_num, 
               MAX_NUM_FORM_COUNT: self.max_num})
        return form

    def total_form_count(self):
        """Returns the total number of forms in this FormSet."""
        if self.is_bound:
            return min(self.management_form.cleaned_data[TOTAL_FORM_COUNT], self.absolute_max)
        initial_forms = self.initial_form_count()
        total_forms = max(initial_forms, self.min_num) + self.extra
        if initial_forms > self.max_num >= 0:
            total_forms = initial_forms
        elif total_forms > self.max_num >= 0:
            total_forms = self.max_num
        return total_forms

    def initial_form_count(self):
        """Returns the number of forms that are required in this FormSet."""
        if self.is_bound:
            return self.management_form.cleaned_data[INITIAL_FORM_COUNT]
        initial_forms = len(self.initial) if self.initial else 0
        return initial_forms

    @cached_property
    def forms(self):
        """
        Instantiate forms at first property access.
        """
        forms = [ self._construct_form(i, **self.get_form_kwargs(i)) for i in range(self.total_form_count())
                ]
        return forms

    def get_form_kwargs(self, index):
        """
        Return additional keyword arguments for each individual formset form.

        index will be None if the form being constructed is a new empty
        form.
        """
        return self.form_kwargs.copy()

    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {b'auto_id': self.auto_id, 
           b'prefix': self.add_prefix(i), 
           b'error_class': self.error_class, 
           b'use_required_attribute': False}
        if self.is_bound:
            defaults[b'data'] = self.data
            defaults[b'files'] = self.files
        if self.initial and b'initial' not in kwargs:
            try:
                defaults[b'initial'] = self.initial[i]
            except IndexError:
                pass

        if i >= self.initial_form_count() and i >= self.min_num:
            defaults[b'empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form

    @property
    def initial_forms(self):
        """Return a list of all the initial forms in this formset."""
        return self.forms[:self.initial_form_count()]

    @property
    def extra_forms(self):
        """Return a list of all the extra forms in this formset."""
        return self.forms[self.initial_form_count():]

    @property
    def empty_form(self):
        form = self.form(auto_id=self.auto_id, prefix=self.add_prefix(b'__prefix__'), empty_permitted=True, use_required_attribute=False, **self.get_form_kwargs(None))
        self.add_fields(form, None)
        return form

    @property
    def cleaned_data(self):
        """
        Returns a list of form.cleaned_data dicts for every form in self.forms.
        """
        if not self.is_valid():
            raise AttributeError(b"'%s' object has no attribute 'cleaned_data'" % self.__class__.__name__)
        return [ form.cleaned_data for form in self.forms ]

    @property
    def deleted_forms(self):
        """
        Returns a list of forms that have been marked for deletion.
        """
        if not self.is_valid() or not self.can_delete:
            return []
        if not hasattr(self, b'_deleted_form_indexes'):
            self._deleted_form_indexes = []
            for i in range(0, self.total_form_count()):
                form = self.forms[i]
                if i >= self.initial_form_count() and not form.has_changed():
                    continue
                if self._should_delete_form(form):
                    self._deleted_form_indexes.append(i)

        return [ self.forms[i] for i in self._deleted_form_indexes ]

    @property
    def ordered_forms(self):
        """
        Returns a list of form in the order specified by the incoming data.
        Raises an AttributeError if ordering is not allowed.
        """
        if not self.is_valid() or not self.can_order:
            raise AttributeError(b"'%s' object has no attribute 'ordered_forms'" % self.__class__.__name__)
        if not hasattr(self, b'_ordering'):
            self._ordering = []
            for i in range(0, self.total_form_count()):
                form = self.forms[i]
                if i >= self.initial_form_count() and not form.has_changed():
                    continue
                if self.can_delete and self._should_delete_form(form):
                    continue
                self._ordering.append((i, form.cleaned_data[ORDERING_FIELD_NAME]))

            def compare_ordering_key(k):
                if k[1] is None:
                    return (1, 0)
                else:
                    return (
                     0, k[1])

            self._ordering.sort(key=compare_ordering_key)
        return [ self.forms[i[0]] for i in self._ordering ]

    @classmethod
    def get_default_prefix(cls):
        return b'form'

    def non_form_errors(self):
        """
        Returns an ErrorList of errors that aren't associated with a particular
        form -- i.e., from formset.clean(). Returns an empty ErrorList if there
        are none.
        """
        if self._non_form_errors is None:
            self.full_clean()
        return self._non_form_errors

    @property
    def errors(self):
        """
        Returns a list of form.errors for every form in self.forms.
        """
        if self._errors is None:
            self.full_clean()
        return self._errors

    def total_error_count(self):
        """
        Returns the number of errors across all forms in the formset.
        """
        return len(self.non_form_errors()) + sum(len(form_errors) for form_errors in self.errors)

    def _should_delete_form(self, form):
        """
        Returns whether or not the form was marked for deletion.
        """
        return form.cleaned_data.get(DELETION_FIELD_NAME, False)

    def is_valid(self):
        """
        Returns True if every form in self.forms is valid.
        """
        if not self.is_bound:
            return False
        forms_valid = True
        self.errors
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            if self.can_delete:
                if self._should_delete_form(form):
                    continue
            forms_valid &= form.is_valid()

        return forms_valid and not self.non_form_errors()

    def full_clean(self):
        """
        Cleans all of self.data and populates self._errors and
        self._non_form_errors.
        """
        self._errors = []
        self._non_form_errors = self.error_class()
        empty_forms_count = 0
        if not self.is_bound:
            return
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            if not form.has_changed() and i >= self.initial_form_count():
                empty_forms_count += 1
            self._errors.append(form.errors)

        try:
            if self.validate_max and self.total_form_count() - len(self.deleted_forms) > self.max_num or self.management_form.cleaned_data[TOTAL_FORM_COUNT] > self.absolute_max:
                raise ValidationError(ungettext(b'Please submit %d or fewer forms.', b'Please submit %d or fewer forms.', self.max_num) % self.max_num, code=b'too_many_forms')
            if self.validate_min and self.total_form_count() - len(self.deleted_forms) - empty_forms_count < self.min_num:
                raise ValidationError(ungettext(b'Please submit %d or more forms.', b'Please submit %d or more forms.', self.min_num) % self.min_num, code=b'too_few_forms')
            self.clean()
        except ValidationError as e:
            self._non_form_errors = self.error_class(e.error_list)

    def clean(self):
        """
        Hook for doing any extra formset-wide cleaning after Form.clean() has
        been called on every form. Any ValidationError raised by this method
        will not be associated with a particular form; it will be accessible
        via formset.non_form_errors()
        """
        pass

    def has_changed(self):
        """
        Returns true if data in any form differs from initial.
        """
        return any(form.has_changed() for form in self)

    def add_fields(self, form, index):
        """A hook for adding extra fields on to each form instance."""
        if self.can_order:
            if index is not None and index < self.initial_form_count():
                form.fields[ORDERING_FIELD_NAME] = IntegerField(label=_(b'Order'), initial=index + 1, required=False)
            else:
                form.fields[ORDERING_FIELD_NAME] = IntegerField(label=_(b'Order'), required=False)
        if self.can_delete:
            form.fields[DELETION_FIELD_NAME] = BooleanField(label=_(b'Delete'), required=False)
        return

    def add_prefix(self, index):
        return b'%s-%s' % (self.prefix, index)

    def is_multipart(self):
        """
        Returns True if the formset needs to be multipart, i.e. it
        has FileInput. Otherwise, False.
        """
        if self.forms:
            return self.forms[0].is_multipart()
        else:
            return self.empty_form.is_multipart()

    @property
    def media(self):
        if self.forms:
            return self.forms[0].media
        else:
            return self.empty_form.media

    def as_table(self):
        """Returns this formset rendered as HTML <tr>s -- excluding the <table></table>."""
        forms = (b' ').join(form.as_table() for form in self)
        return mark_safe((b'\n').join([six.text_type(self.management_form), forms]))

    def as_p(self):
        """Returns this formset rendered as HTML <p>s."""
        forms = (b' ').join(form.as_p() for form in self)
        return mark_safe((b'\n').join([six.text_type(self.management_form), forms]))

    def as_ul(self):
        """Returns this formset rendered as HTML <li>s."""
        forms = (b' ').join(form.as_ul() for form in self)
        return mark_safe((b'\n').join([six.text_type(self.management_form), forms]))


def formset_factory(form, formset=BaseFormSet, extra=1, can_order=False, can_delete=False, max_num=None, validate_max=False, min_num=None, validate_min=False):
    """Return a FormSet for the given form class."""
    if min_num is None:
        min_num = DEFAULT_MIN_NUM
    if max_num is None:
        max_num = DEFAULT_MAX_NUM
    absolute_max = max_num + DEFAULT_MAX_NUM
    attrs = {b'form': form, b'extra': extra, b'can_order': can_order, 
       b'can_delete': can_delete, b'min_num': min_num, 
       b'max_num': max_num, b'absolute_max': absolute_max, 
       b'validate_min': validate_min, b'validate_max': validate_max}
    return type(form.__name__ + str(b'FormSet'), (formset,), attrs)


def all_valid(formsets):
    """Returns true if every formset in formsets is valid."""
    valid = True
    for formset in formsets:
        if not formset.is_valid():
            valid = False

    return valid