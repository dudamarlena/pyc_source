# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/r/prj/p/dosca/env/lib/python3.5/site-packages/dosca/ext.py
# Compiled at: 2015-07-07 19:42:11
# Size of source mod 2**32: 1379 bytes
from itertools import chain
from . import dosca
YES_NO_BOOL = [
 (
  lambda x: x.lower() == 'yes', lambda _: True),
 (
  lambda x: x.lower() == 'no', lambda _: False)]
ON_OFF_BOOL = [
 (
  lambda x: x.lower() == 'on', lambda _: True),
 (
  lambda x: x.lower() == 'off', lambda _: False)]

def PHP_ARRAYS(section, key, value):
    if key.endswith('[]'):
        if key in section:
            section[key].append(value)
        else:
            section[key] = [
             value]
        return True


def make_parse(*extensions):
    ext_parsers = []
    ext_hooks = []
    for ext in extensions:
        for item in ext:
            if isinstance(item, tuple):
                ext_parsers.append(item)
            elif callable(item):
                ext_hooks.append(item)

    def parse(fileobj, custom_parsers=[], key_hooks=[]):
        ep = list(ext_parsers)
        ep.extend(custom_parsers)
        eh = list(ext_hooks)
        eh.extend(key_hooks)
        return dosca.parse(fileobj, custom_parsers=ep, key_hooks=eh)

    return parse


def make_parse_file(*extensions):
    parse = make_parse_file(*extensions)

    def parse_file(fileobj, custom_parsers=[], key_hooks=[]):
        with open(filename) as (fileobj):
            return parse(fileobj, custom_parsers=custom_parsers, key_hooks=key_hooks)

    return parse_file