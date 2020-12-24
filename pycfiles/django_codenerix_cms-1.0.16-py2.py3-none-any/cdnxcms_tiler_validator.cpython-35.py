# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/templatetags/cdnxcms_tiler_validator.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 3218 bytes
import json
from django import template
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from codenerix_cms.models import VALID_TYPE_TEMPLATE
register = template.Library()

@register.simple_tag(takes_context=True)
def cdnx_tiler_type(context, json_tiler_type):
    response = {'code_error': 0}
    try:
        tiler_type = json.loads(json_tiler_type)
        valid_types = True
        for tag in tiler_type:
            if valid_types and tiler_type[tag] not in VALID_TYPE_TEMPLATE:
                valid_types = False
                response['code_error'] = 4
                response['error_msg'] = _('Type %(tag)s  does not a allowed type. List of allowed are: %(valid)s') % {'tag': tiler_type[tag], 'valid': VALID_TYPE_TEMPLATE}

        if valid_types:
            if 'cdnx_tiler_types' in context:
                context['cdnx_tiler_types'].update(tiler_type)
            else:
                context['cdnx_tiler_types'] = tiler_type
            response['data'] = context['cdnx_tiler_types']
    except ValueError as e:
        response['code_error'] = 1
        response['error_msg'] = _('cdnx_tiler_type has wrong format: %(error)s') % {'error': e}

    return mark_safe(json.dumps(response))


@register.simple_tag(takes_context=True)
def cdnx_tiler(context, fieldkey):
    response = {'code_error': 0}
    if 'cdnx_tiler_types' in context:
        kinds = context['cdnx_tiler_types']
        if fieldkey in kinds.keys():
            response['data'] = {fieldkey: kinds[fieldkey]}
        else:
            response['code_error'] = 2
            response['error_msg'] = _('Field %(field)s has not been declared, I can see only: %(fields)s') % {'field': fieldkey, 'fields': ', '.join(kinds.keys())}
    else:
        response['code_error'] = 3
        response['error_msg'] = _('Any type has been declared.')
    return mark_safe(json.dumps(response))