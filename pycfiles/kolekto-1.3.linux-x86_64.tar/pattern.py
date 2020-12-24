# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/pattern.py
# Compiled at: 2014-06-16 16:12:17
""" Parse and format patterns.
"""
from string import Formatter

def parse_pattern(format_string, env, wrapper=lambda x, y: y):
    """ Parse the format_string and return prepared data according to the env.

    Pick each field found in the format_string from the env(ironment), apply
    the wrapper on each data and return a mapping between field-to-replace and
    values for each.
    """
    formatter = Formatter()
    fields = [ x[1] for x in formatter.parse(format_string) if x[1] is not None ]
    prepared_env = {}
    for field in fields:
        for field_alt in (x.strip() for x in field.split('|')):
            if field_alt[0] in '\'"' and field_alt[(-1)] in '\'"':
                field_values = field_alt[1:-1]
            else:
                field_values = env.get(field_alt)
            if field_values is not None:
                break
        else:
            field_values = []

        if not isinstance(field_values, list):
            field_values = [
             field_values]
        prepared_env[field] = wrapper(field_alt, field_values)

    return prepared_env