# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/templatetags/djblets_js.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import json
from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template.defaultfilters import escapejs
from django.utils import six
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from djblets.util.serializers import DjbletsJSONEncoder
register = template.Library()
_safe_js_escapes = {ord(b'&'): b'\\u0026', 
   ord(b'<'): b'\\u003C', 
   ord(b'>'): b'\\u003E'}

@register.simple_tag
def form_dialog_fields(form):
    """
    Translates a Django Form object into a JavaScript list of fields.
    The resulting list of fields can be used to represent the form
    dynamically.
    """
    s = b''
    for field in form:
        s += b"{ name: '%s', " % escapejs(field.name)
        if field.is_hidden:
            s += b'hidden: true, '
        else:
            s += b"label: '%s', " % escapejs(field.label_tag(field.label + b':'))
            if field.field.required:
                s += b'required: true, '
            if field.field.help_text:
                s += b"help_text: '%s', " % escapejs(field.field.help_text)
        s += b"widget: '%s' }," % escapejs(six.text_type(field))

    return b'[ %s ]' % s[:-1]


@register.filter
def json_dumps(value, indent=None):
    if isinstance(value, QuerySet):
        result = serialize(b'json', value, indent=indent)
    else:
        result = json.dumps(value, indent=indent, cls=DjbletsJSONEncoder)
    return mark_safe(force_text(result).translate(_safe_js_escapes))


@register.filter
def json_dumps_items(d, append=b''):
    """Dumps a list of keys/values from a dictionary, without braces.

    This works very much like ``json_dumps``, but doesn't output the
    surrounding braces. This allows it to be used within a JavaScript
    object definition alongside other custom keys.

    If the dictionary is not empty, and ``append`` is passed, it will be
    appended onto the results. This is most useful when you want to append
    a comma after all the dictionary items, in order to provide further
    keys in the template.
    """
    if not d:
        return b''
    return mark_safe(json_dumps(d)[1:-1] + append)