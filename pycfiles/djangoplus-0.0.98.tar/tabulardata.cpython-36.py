# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/utils/tabulardata.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 1005 bytes
from djangoplus.utils.formatter import format_value
from djangoplus.utils.metadata import get_metadata, get_fiendly_name, getattr2

def tolist(qs, add_header=True, list_display=()):
    model = qs.model
    data = []
    fields = []
    header = []
    if type(list_display) == bool or not list_display:
        list_display = get_metadata(model, 'list_display', fields)
    else:
        if list_display:
            for field_name in list_display:
                header.append(get_fiendly_name(model, field_name))
                fields.append(field_name)

        else:
            for field in get_metadata(model, 'fields'):
                header.append(field.verbose_name)
                fields.append(field.name)

    if add_header:
        data.append(header)
    for obj in qs:
        row = []
        for field in fields:
            val = getattr2(obj, field)
            if callable(val):
                val = val()
            row.append(format_value(val, False))

        data.append(row)

    return data