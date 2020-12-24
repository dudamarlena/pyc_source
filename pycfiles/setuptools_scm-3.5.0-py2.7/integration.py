# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/integration.py
# Compiled at: 2020-02-13 15:05:29
from pkg_resources import iter_entry_points
from .version import _warn_if_setuptools_outdated
from .utils import do, trace_exception
from . import _get_version, Configuration

def version_keyword(dist, keyword, value):
    _warn_if_setuptools_outdated()
    if not value:
        return
    else:
        if value is True:
            value = {}
        if getattr(value, '__call__', None):
            value = value()
        config = Configuration(**value)
        dist.metadata.version = _get_version(config)
        return


def find_files(path=''):
    for ep in iter_entry_points('setuptools_scm.files_command'):
        command = ep.load()
        if isinstance(command, str):
            res = do(ep.load(), path or '.').splitlines()
        else:
            res = command(path)
        if res:
            return res

    return []


def _args_from_toml(name='pyproject.toml'):
    with open(name) as (strm):
        defn = __import__('toml').load(strm)
    return defn.get('tool', {})['setuptools_scm']


def infer_version(dist):
    try:
        config = Configuration.from_file()
    except Exception:
        return trace_exception()

    dist.metadata.version = _get_version(config)