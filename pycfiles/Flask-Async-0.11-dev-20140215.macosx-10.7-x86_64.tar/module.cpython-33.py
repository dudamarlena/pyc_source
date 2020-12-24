# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/module.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 1363 bytes
"""
    flask.module
    ~~~~~~~~~~~~

    Implements a class that represents module blueprints.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import os
from .blueprints import Blueprint

def blueprint_is_module(bp):
    """Used to figure out if something is actually a module"""
    return isinstance(bp, Module)


class Module(Blueprint):
    __doc__ = 'Deprecated module support.  Until Flask 0.6 modules were a different\n    name of the concept now available as blueprints in Flask.  They are\n    essentially doing the same but have some bad semantics for templates and\n    static files that were fixed with blueprints.\n\n    .. versionchanged:: 0.7\n       Modules were deprecated in favor for blueprints.\n    '

    def __init__(self, import_name, name=None, url_prefix=None, static_path=None, subdomain=None):
        if name is None:
            assert '.' in import_name, 'name required if package name does not point to a submodule'
            name = import_name.rsplit('.', 1)[1]
        Blueprint.__init__(self, name, import_name, url_prefix=url_prefix, subdomain=subdomain, template_folder='templates')
        if os.path.isdir(os.path.join(self.root_path, 'static')):
            self._static_folder = 'static'
        return