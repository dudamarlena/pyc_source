# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eric/Documents/code/django-cartodb-sync/cartodbsync/synchronize.py
# Compiled at: 2015-10-11 16:51:50
# Size of source mod 2**32: 872 bytes
from importlib import import_module
from django.apps import apps
from django.conf import settings

def get_model(model_string):
    return apps.get_model(*model_string.split('.'))


def get_synchronizer_class(synchronizer_string):
    module_name, class_name = synchronizer_string.rsplit('.', 1)
    return getattr(import_module(module_name), class_name)


def synchronize_settings_entry(settings_entry):
    model = get_model(settings_entry['MODEL_CLASS'])
    synchronizer_class = get_synchronizer_class(settings_entry['SYNCHRONIZER_CLASS'])
    synchronizer = synchronizer_class(model, settings_entry['CARTODB_TABLE'])
    synchronizer.synchronize()


def synchronize(model_name=None):
    for m in settings.CARTODB_SYNC['MODELS']:
        if model_name and model_name != m['MODEL_CLASS']:
            continue
        else:
            synchronize_settings_entry(m)