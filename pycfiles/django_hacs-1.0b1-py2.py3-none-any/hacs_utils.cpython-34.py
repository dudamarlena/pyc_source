# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/templatetags/hacs_utils.py
# Compiled at: 2016-06-10 13:10:03
# Size of source mod 2**32: 1138 bytes
from __future__ import unicode_literals
import ast, json
from django.utils import six
from django.template import Library
from django.template import TemplateSyntaxError
from django.core.serializers.json import DjangoJSONEncoder
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'
register = Library()

@register.filter(is_safe=False)
def to_json(value):
    """
    This method will make JSON like string from any string value that is made from list oo dict object
    :param value:
    :return:
    """
    if not value:
        return ''
    try:
        if isinstance(value, six.string_types):
            value = ast.literal_eval(value)
    except ValueError as exc:
        try:
            json.loads(value)
            return value
        except ValueError:
            pass

        raise TemplateSyntaxError('string must be made from dict or list or tuple object. Original message: %s' % exc)
    else:
        return json.dumps(value, cls=DjangoJSONEncoder)