# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mobiclicks/conf.py
# Compiled at: 2013-11-28 10:36:39
import sys
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
defaults = {'CPA_TOKEN_SESSION_KEY': 'mobiclicks_cpatoken', 
   'CPA_TOKEN_PARAMETER_NAME': 'cpa', 
   'CLICK_REF_PARAMETER_NAME': 'pollen8_click_ref', 
   'CPA_SECURITY_TOKEN': None, 
   'ACQUISITION_TRACKING_URL': 'http://t.mobiclicksdirect.com/acquisition', 
   'CLICK_CONFIRMATION_URL': 'http://t.mobiclicksdirect.com/advertiser', 
   'TRACK_REGISTRATIONS': True, 
   'CONFIRM_CLICKS': True}

def init_configuration():
    settings_dict = getattr(settings, 'MOBICLICKS', {})
    for key, default_value in defaults.iteritems():
        setattr(sys.modules[__name__], key, settings_dict.get(key, defaults[key]))


def validate_configuration():
    if CPA_SECURITY_TOKEN is None:
        raise ImproperlyConfigured("Setting MOBICLICKS['CPA_SECURITY_TOKEN'] is required")
    from django.db.models.fields import DateTimeField, FieldDoesNotExist
    try:
        from django.contrib.auth import get_user_model
    except ImportError:
        from django.contrib.auth.models import User
    else:
        User = get_user_model()

    try:
        field = User._meta.get_field_by_name('date_joined')
        if not isinstance(field[0], DateTimeField):
            raise TypeError
    except (FieldDoesNotExist, TypeError):
        raise ImproperlyConfigured('The current User model does not have the required field <django.db.models.fields.DateTimeField: date_joined>')

    return


init_configuration()