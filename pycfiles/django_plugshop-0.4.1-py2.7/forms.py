# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/forms.py
# Compiled at: 2016-12-25 15:56:13
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from plugshop import settings
from plugshop.utils import get_model
PRODUCT_CLASS = get_model(settings.PRODUCT_MODEL)
ORDER_CLASS = get_model(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = get_model(settings.ORDER_PRODUCTS_MODEL)
NAME_ERROR = _('Name is required')
EMAIL_ERROR = _('Invalid email address')
EMAIL_ERROR_EXISTS = _("Email address '%s' already exits, must be unique")

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=PRODUCT_CLASS.objects)
    quantity = forms.IntegerField(required=False)


class OrderForm(forms.ModelForm):

    class Meta:
        model = ORDER_CLASS
        exclude = ('number', 'status', 'created_at', 'updated_at', 'user', 'products')

    name = forms.CharField(required=True, error_messages={'required': NAME_ERROR})
    email = forms.EmailField(required=True, error_messages={'required': EMAIL_ERROR})

    def save(self, commit=True, **kwargs):
        cart = kwargs.get('cart')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name', '')
        last_name = self.cleaned_data.get('last_name', '')
        user, created = User.objects.get_or_create(username=email, defaults={'email': email, 
           'first_name': first_name, 
           'last_name': last_name, 
           'is_active': False})
        model = super(OrderForm, self).save(commit=False)
        model.user = user
        if commit:
            model.save()
            for c in cart:
                ORDER_PRODUCTS_CLASS.objects.create(product=c.product, quantity=c.quantity, order=model)

        return model

    def clean_name(self):
        name = self.cleaned_data.get('name').strip()
        if len(name):
            n = name.split()
            if len(n) > 1:
                self.cleaned_data['first_name'] = (' ').join(n[1:])
                self.cleaned_data['last_name'] = n[0]
            else:
                self.cleaned_data['first_name'] = name
                self.cleaned_data['last_name'] = ''
        else:
            raise forms.ValidationError(NAME_ERROR)
        return name