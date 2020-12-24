# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/forms_special_fields.py
# Compiled at: 2019-11-08 17:24:24
# Size of source mod 2**32: 11265 bytes
from django import forms
from django.core.validators import ValidationError
from django.utils.encoding import smart_str
from django.forms.renderers import get_default_renderer
from NearBeach.models import product_and_service, list_of_country_region, list_of_country, customer, organisation
from django.utils.html import escape, mark_safe
import gettext

class ConnectCustomerSelect(forms.SelectMultiple):
    __doc__ = '\n    We want the ability to render a multiple select in a table format. This will give the use a friendly layout.\n    The fields we want are;\n    -- Tickbox\n    -- Customer First Name\n    -- Customer Last Name\n    -- Customer organisation (if any)\n    '

    def _render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        customer_results = customer.objects.filter(is_deleted='FALSE').order_by('customer_first_name', 'customer_last_name')
        output = '<table class="table table-hover table-striped mt-4"><thead><tr><td> - </td><td>Customer First Name</td><td>Customer Last Name</td><td>Customer Organisation</td><tr></thead>'
        for idx, row in enumerate(customer_results):
            if row.organisation_id:
                output = output + '<tr><td><input type="checkbox" id="id_customers_%s" name="customers" value="%s"></td>' % (str(idx), str(row.customer_id)) + '<td>%s</td>' % row.customer_first_name + '<td>%s</td>' % row.customer_last_name + '<td>%s</td>' % str(row.organisation_id) + '</tr>'
            else:
                output = output + '<tr><td><input type="checkbox" id="id_customers_%s" name="customers" value="%s"></td>' % (str(row.customer_id), str(row.customer_id)) + '<td>%s</td>' % row.customer_first_name + '<td>%s</td>' % row.customer_last_name + '<td>%s</td>' % str(row.organisation_id) + '</tr>'

        output = output + '</table>'
        return output

    def clean(self, value):
        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = ''
        value = forms.util.smart_str(value)
        if value == '':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]

        if value not in valid_values:
            raise ValidationError(gettext('Select a valid choice. That choice is not one of the available choices.'))
        return value


class ConnectOrganisationSelect(forms.SelectMultiple):
    __doc__ = '\n    We want the ability to render a multiple select in a table format. This will give the use a friendly layout.\n    The fields we want are;\n    -- Tickbox\n    -- Organisation Name\n    -- Organisation Website\n    -- Organisation Email\n    '

    def _render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        organisation_results = organisation.objects.filter(is_deleted='FALSE').order_by('organisation_name')
        output = '<table class="table table-hover table-striped mt-4"><thead><tr><td> - </td><td>Organisation Name</td><td>Organisation Website</td><td>Organisation Email</td><tr></thead>'
        for idx, row in enumerate(organisation_results):
            output = output + '<tr><td><input type="checkbox" id="id_organisations_%s" name="organisations" value="%s"></td>' % (str(row.organisation_id), str(row.organisation_id)) + '<td>%s</td>' % row.organisation_name + '<td>%s</td>' % row.organisation_website + '<td>%s</td>' % str(row.organisation_email) + '</tr>'

        output = output + '</table>'
        return output

    def clean(self, value):
        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = ''
        value = forms.util.smart_str(value)
        if value == '':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]

        if value not in valid_values:
            raise ValidationError(gettext('Select a valid choice. That choice is not one of the available choices.'))
        return value


class RegionSelect(forms.Select):
    __doc__ = '\n    Regional Select is a dropdown widget for selecting both\n    - Region\n    - Country\n    '

    def _render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        country_results = list_of_country.objects.filter(is_deleted='FALSE').order_by('country_name')
        region_results = list_of_country_region.objects.filter(is_deleted='FALSE').order_by('country_id', 'region_name')
        output = '<select name="country_and_regions" id="id_country_and_regions" class="chosen-select form-control"><option value="" selected> Select a Country/Region </option>'
        for country in country_results:
            output = output + '<optgroup label="' + country.country_name + '">'
            for region in region_results.filter(country_id=(country.country_id)):
                option_value = smart_str(region.region_id)
                option_label = smart_str(region.region_name)
                output = output + '<option value="%s">%s' % (escape(option_value), escape(option_label))
                output = output + '</option>'

        output = output + '</optgroup></option></select>'
        return output

    def clean(self, value):
        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = ''
        value = forms.util.smart_str(value)
        if value == '':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]

        if value not in valid_values:
            raise ValidationError(gettext('Select a valid choice. That choice is not one of the available choices.'))
        return value


class ToEmailSelect(forms.SelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        customer_results = customer.objects.filter(is_deleted='FALSE')
        output = '<select name="to_email" id="id_to_email" class="chosen-select form-control"><option value="------" selected disabled> Select an Email </option>'
        for option in customer_results:
            option_value = smart_str(option.customer_id)
            option_label = smart_str(option.customer_email)
            output = output + '<option value="%s">%s' % (escape(option_value), escape(option_label))
            output = output + '</option>'

        output = output + '</select>'
        return output

    def clean(self, value):
        value = super(forms.ChoiceField, self).clean(value)
        if value in (None, ''):
            value = ''
        value = forms.util.smart_str(value)
        if value == '':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]

        if value not in valid_values:
            raise ValidationError(gettext('Select a valid choice. That choice is not one of the available choices.'))
        return value