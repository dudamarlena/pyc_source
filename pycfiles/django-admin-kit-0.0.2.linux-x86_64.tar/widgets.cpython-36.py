# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rohan/Django/django-admin-kit/.venv/lib/python3.6/site-packages/admin_kit/widgets.py
# Compiled at: 2017-11-30 08:44:30
# Size of source mod 2**32: 1722 bytes
"""
    Admin Kit Widgets module

"""
import json
from django.forms.widgets import SelectMultiple, Select
__all__ = [
 'SelectMultipleWidget', 'SelectWidget']

class SelectMultipleWidget(SelectMultiple):
    __doc__ = "\n    MultiSelect Widget which inherits Django's SelectMultiple widget\n\n    "
    template_name = 'admin_kit/widgets/select.html'
    option_template_name = 'admin_kit/widgets/select_option.html'

    class Media:
        __doc__ = "\n        This class adds css required for admin_kit's widget\n\n        "
        css = {'all': ('admin_kit/css/select.css', )}

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'admin-kit admin-kit-select'
        kit_config = json.loads(context['widget']['attrs']['data-kit-config'])
        kit_config['init-value'] = ','.join(context['widget']['value'])
        context['widget']['attrs']['data-kit-config'] = json.dumps(kit_config)
        return context


class SelectWidget(Select):
    __doc__ = "\n    MultiSelect Widget which inherits Django's Select widget\n\n    "

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'admin-kit admin-kit-select'
        kit_config = json.loads(context['widget']['attrs']['data-kit-config'])
        kit_config['init-value'] = ','.join(context['widget']['value'])
        context['widget']['attrs']['data-kit-config'] = json.dumps(kit_config)
        return context