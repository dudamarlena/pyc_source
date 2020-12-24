# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fatfrog/Documents/backmap/.eggs/setuptools_scm-2.0.0-py3.6.egg/setuptools_scm/integration.py
# Compiled at: 2018-04-13 13:17:12
# Size of source mod 2**32: 1183 bytes
import os
from .version import _warn_if_setuptools_outdated
from .utils import do
from .discover import iter_matching_entrypoints
from . import get_version

def version_keyword(dist, keyword, value):
    _warn_if_setuptools_outdated()
    if not value:
        return
    if value is True:
        value = {}
    if getattr(value, '__call__', None):
        value = value()
    matching_fallbacks = iter_matching_entrypoints('.', 'setuptools_scm.parse_scm_fallback')
    if any(matching_fallbacks):
        value.pop('root', None)
    dist.metadata.version = get_version(**value)


def find_files(path='.'):
    if not path:
        path = '.'
    else:
        abs = os.path.abspath(path)
        ep = next(iter_matching_entrypoints(abs, 'setuptools_scm.files_command'), None)
        if ep:
            command = ep.load()
            try:
                if isinstance(command, str):
                    return do(ep.load(), path).splitlines()
                else:
                    return command(path)
            except Exception:
                print('File Finder Failed for %s' % ep)
                raise

        else:
            return []