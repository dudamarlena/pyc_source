# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dnavarro/repos/django-leads/leads/utils.py
# Compiled at: 2014-02-26 09:41:22
# Size of source mod 2**32: 877 bytes
from importlib import import_module
from django.conf import settings

def get_class_from_string(import_string):
    try:
        from_list, import_name = import_string.rsplit('.', 1)
        return getattr(import_module(from_list), import_name)
    except (AttributeError, ValueError):
        raise ImportError(import_string)


def get_register_model():
    return get_class_from_string(getattr(settings, 'LEADS_REGISTER_MODEL', 'leads.models.Register'))


def get_register_model_admin():
    return get_class_from_string(getattr(settings, 'LEADS_REGISTER_MODEL_ADMIN', 'leads.admin.RegisterAdmin'))


def get_register_form_class():
    return get_class_from_string(getattr(settings, 'LEADS_REGISTER_FORM_CLASS', 'leads.forms.RegisterForm'))


def get_register_form_fields():
    return getattr(settings, 'LEADS_REGISTER_FORM_FIELDS', ('name', 'email'))