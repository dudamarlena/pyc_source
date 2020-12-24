# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adminlteui/templatetags/adminlte_options.py
# Compiled at: 2020-05-05 22:21:28
# Size of source mod 2**32: 1954 bytes
import traceback
from django import template
from adminlteui.models import Options
from adminlteui import version
from django.conf import settings
register = template.Library()

@register.simple_tag
def get_adminlte_option(option_name, request=None):
    config_ = {}
    config_list = Options.objects.filter(valid=True)
    if config_list.filter(option_name=option_name):
        config_[option_name] = config_list.get(option_name=option_name).option_value
        if request:
            if option_name == 'avatar_field':
                try:
                    image_path = eval(config_[option_name]).name
                    if image_path:
                        config_[option_name] = settings.MEDIA_URL + image_path
                    else:
                        config_[option_name] = None
                except Exception as e:
                    traceback.print_exc()
                    config_[option_name] = None

        config_['valid'] = config_list.get(option_name=option_name).valid
    return config_


@register.simple_tag
def get_adminlte_settings():
    if hasattr(settings, 'ADMINLTE_SETTINGS'):
        return settings.ADMINLTE_SETTINGS
    else:
        return {'demo':True, 
         'search_form':True, 
         'icons':{'myapp': {'shops':'fa-shopping-cart', 
                    'products':'fa-dollar'}}}


@register.simple_tag
def get_adminlte_version():
    return version