# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/conf/env.py
# Compiled at: 2015-01-27 01:44:29
# Size of source mod 2**32: 1031 bytes
import os, ast, re
__all__ = [
 'get']
_cache = None

def get_cache():
    global _cache
    if _cache is None:
        _cache = {}
        _update(os.environ)
        try:
            env_file = os.path.abspath(os.path.join(os.environ['VIRTUAL_ENV'], '../.env'))
        except KeyError:
            pass
        else:
            if os.path.exists(env_file):
                load_file(env_file)
            return _cache


def _set(key, value):
    _cache[key] = value


def _update(values):
    for key in values:
        _set(key, values[key])


def load_file(path):
    result = {}
    with open(path) as (fh):
        content = fh.read()
        for line in content.splitlines():
            values = re.findall('\\s*(\\w+)\\s*=\\s*(.+)\\s*', line)
            if values:
                key, value = values[0]
                result[key] = value.strip()

    _update(result)


def get(key, default=None):
    cache = get_cache()
    return cache.get(key, default)


def all():
    cache = get_cache()
    return cache.copy()