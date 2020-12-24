# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/template/loaders/namespaced_app_dirs.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import os
from importlib import import_module
from django.template import TemplateDoesNotExist
from django.template.loaders import app_directories

class Loader(app_directories.Loader):
    """Looks for templates in app directories, optionally with a namespace.

    This extends the standard Django 'app_directories' template loader by
    allowing a prefix specifying the app whose template should be used.
    It solves the problem of one app defining a template and another app
    trying to both override and extend it, resulting in an infinite loop.

    Templates can be in the standard form of 'path/to/template', or in the
    namespaced form of 'app.path:path/to/template'.
    """

    def __init__(self, *args, **kwargs):
        super(Loader, self).__init__(*args, **kwargs)
        self._cache = {}

    def get_template_sources(self, template_name, template_dirs=None):
        parts = template_name.split(b':')
        if len(parts) == 2:
            app = parts[0]
            template_dir = self._cache.get(app)
            if not template_dir:
                try:
                    mod = import_module(app)
                except ImportError:
                    raise TemplateDoesNotExist(template_name)

                template_dir = os.path.join(os.path.dirname(mod.__file__), b'templates')
                self._cache[app] = template_dir
            template_name = parts[1]
            template_dirs = [template_dir]
        return super(Loader, self).get_template_sources(template_name, template_dirs)