# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/template/loaders/app_directories.py
# Compiled at: 2018-07-11 18:15:31
"""
Wrapper for loading templates from "templates" directories in INSTALLED_APPS
packages.
"""
import os, sys
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join
from django.utils.importlib import import_module
from django.utils import six
if not six.PY3:
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
app_template_dirs = []
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError as e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))

    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    if os.path.isdir(template_dir):
        if not six.PY3:
            template_dir = template_dir.decode(fs_encoding)
        app_template_dirs.append(template_dir)

app_template_dirs = tuple(app_template_dirs)

class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        if not template_dirs:
            template_dirs = app_template_dirs
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except UnicodeDecodeError:
                raise
            except ValueError:
                pass

    def load_template_source(self, template_name, template_dirs=None):
        for filepath in self.get_template_sources(template_name, template_dirs):
            try:
                with open(filepath, 'rb') as (fp):
                    return (
                     fp.read().decode(settings.FILE_CHARSET), filepath)
            except IOError:
                pass

        raise TemplateDoesNotExist(template_name)