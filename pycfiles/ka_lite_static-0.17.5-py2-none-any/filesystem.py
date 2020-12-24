# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/template/loaders/filesystem.py
# Compiled at: 2018-07-11 18:15:31
"""
Wrapper for loading templates from the filesystem.
"""
from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join

class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except UnicodeDecodeError:
                raise
            except ValueError:
                pass

    def load_template_source(self, template_name, template_dirs=None):
        tried = []
        for filepath in self.get_template_sources(template_name, template_dirs):
            try:
                with open(filepath, 'rb') as (fp):
                    return (
                     fp.read().decode(settings.FILE_CHARSET), filepath)
            except IOError:
                tried.append(filepath)

        if tried:
            error_msg = 'Tried %s' % tried
        else:
            error_msg = 'Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory.'
        raise TemplateDoesNotExist(error_msg)

    load_template_source.is_usable = True