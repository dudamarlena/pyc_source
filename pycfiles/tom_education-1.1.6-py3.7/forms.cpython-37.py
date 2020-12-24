# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/forms.py
# Compiled at: 2019-09-30 06:45:25
# Size of source mod 2**32: 3518 bytes
from django import forms
from django.core.exceptions import ValidationError
from tom_dataproducts.models import DataProduct, DataProductGroup
from tom_education.models import ObservationTemplate

def make_templated_form(base_class):
    """
    Return a sub-class of `base_class` which additionally provides links to
    create and instantiate templates.

    `base_class` should be a sub-class of
    tom_observations.facility.GenericObservationForm.
    """

    class F(base_class):
        new_template_action = ('create-template', 'Create new template')

        def __init__(self, *args, **kwargs):
            self.form_url = kwargs.pop('form_url')
            self.show_create = kwargs.pop('show_create')
            (super().__init__)(*args, **kwargs)
            if hasattr(self, 'helper'):
                self.helper.form_tag = None

        def get_extra_context(self):
            context = super().get_extra_context()
            templates = ObservationTemplate.objects.filter(target__pk=(self.initial['target_id']),
              facility=(self.initial['facility']))
            context['templates'] = []
            for template in templates:
                url = template.get_create_url(self.form_url)
                name = template.name
                context['templates'].append((name, url))

            context['show_new_template_action'] = self.show_create
            context['new_template_action_button'] = self.new_template_action
            return context

    return F


class DataProductSelectionForm(forms.Form):
    __doc__ = "\n    Base class for a form including a list of data product checkboxes, where\n    the list of data products is taken from the 'products' kwarg to __init__\n    "

    def __init__(self, *args, **kwargs):
        products = kwargs.pop('products')
        (super().__init__)(*args, **kwargs)
        self.product_pks = set([])
        for dp in products:
            str_pk = str(dp.pk)
            self.product_pks.add(str_pk)
            self.fields[str_pk] = forms.fields.BooleanField(required=False)

    def clean(self):
        if not any((self.cleaned_data.get(str_pk) for str_pk in self.product_pks)):
            raise ValidationError('No data product selected')

    def get_selected_products(self):
        """
        Return the set of products that were selected
        """
        return {DataProduct.objects.get(pk=(int(str_pk))) for str_pk, checked in self.cleaned_data.items() if checked}


class DataProductActionForm(DataProductSelectionForm):
    __doc__ = '\n    Form for selecting a group of data products from the target page to perform\n    some action on them\n    '
    action = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        target = kwargs.pop('target')
        (super().__init__)(args, **kwargs, **{'products': target.dataproduct_set.all()})


class GalleryForm(DataProductSelectionForm):
    __doc__ = '\n    Form for a user to add a selection of data products to a data product group\n    '
    group = forms.ModelChoiceField(DataProductGroup.objects.all())