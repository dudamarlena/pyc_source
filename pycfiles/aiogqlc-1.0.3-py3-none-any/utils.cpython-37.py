# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/aiogql/utils.py
# Compiled at: 2020-01-21 09:02:42
# Size of source mod 2**32: 675 bytes
import re

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(((x.title() if x else '_') for x in components[1:]))


def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', name)
    return re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1).lower()


def to_const(string):
    return re.sub('[\\W|^]+', '_', string).upper()