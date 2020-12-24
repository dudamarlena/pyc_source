# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertbanagale/code/opensource/django-address/django-address/example_site/address/forms.py
# Compiled at: 2020-05-10 01:24:31
import logging, sys
from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from .models import Address, to_python
from .widgets import AddressWidget
if sys.version > '3':
    long = int
    basestring = (str, bytes)
    unicode = str
logger = logging.getLogger(__name__)
__all__ = [
 'AddressWidget', 'AddressField']
if not settings.GOOGLE_API_KEY:
    raise ImproperlyConfigured('GOOGLE_API_KEY is not configured in settings.py')

class AddressField(forms.ModelChoiceField):
    widget = AddressWidget

    def __init__(self, *args, **kwargs):
        kwargs['queryset'] = Address.objects.none()
        super(AddressField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None or value == '':
            return
        for field in ['latitude', 'longitude']:
            if field in value:
                if value[field]:
                    try:
                        value[field] = float(value[field])
                    except Exception:
                        raise forms.ValidationError('Invalid value for %(field)s', code='invalid', params={'field': field})

                else:
                    value[field] = None

        return to_python(value)