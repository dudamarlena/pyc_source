# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/project_template_loader/loaders/project_directory.py
# Compiled at: 2009-12-06 10:03:37
"""Loader to retrieve modules from a 'templates' directory within the project
directory"""
import os, os.path
from django.conf import settings, ENVIRONMENT_VARIABLE as ENV
from django.template import TemplateDoesNotExist
from django.utils._os import safe_join
from django.utils.importlib import import_module
try:
    if not os.environ[ENV]:
        raise ValueError
except (KeyError, ValueError):
    raise ImportError('Settings cannot be imported, because environment variable %s is undefined.' % ENV)

settings_module = import_module(os.environ[ENV])

def get_template_sources(template_name, template_dirs=None):
    if template_dirs is None:
        template_dirs = []
    for template_dir in template_dirs:
        try:
            template_path = safe_join(template_dir, template_name)
            yield template_path
        except UnicodeDecodeError:
            raise
        except ValueError:
            pass

    return


def load_template_source(template_name, template_dirs=None):
    if not template_dirs:
        project_dir = os.path.dirname(settings_module.__file__)
        project_template_dir = os.path.join(project_dir, 'templates')
        template_dirs = [project_template_dir]
    for filepath in get_template_sources(template_name, template_dirs):
        try:
            return (
             open(filepath).read().decode(settings.FILE_CHARSET),
             filepath)
        except IOError:
            pass

    raise TemplateDoesNotExist, template_name


load_template_source.is_usable = True