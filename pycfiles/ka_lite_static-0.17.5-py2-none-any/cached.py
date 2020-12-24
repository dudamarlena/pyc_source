# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/template/loaders/cached.py
# Compiled at: 2018-07-11 18:15:31
"""
Wrapper class that takes a list of template loaders as an argument and attempts
to load templates from them in order, caching the result.
"""
import hashlib
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader, get_template_from_string, find_template_loader, make_origin
from django.utils.encoding import force_bytes

class Loader(BaseLoader):
    is_usable = True

    def __init__(self, loaders):
        self.template_cache = {}
        self._loaders = loaders
        self._cached_loaders = []

    @property
    def loaders(self):
        if not self._cached_loaders:
            cached_loaders = []
            for loader in self._loaders:
                cached_loaders.append(find_template_loader(loader))

            self._cached_loaders = cached_loaders
        return self._cached_loaders

    def find_template(self, name, dirs=None):
        for loader in self.loaders:
            try:
                template, display_name = loader(name, dirs)
                return (template, make_origin(display_name, loader, name, dirs))
            except TemplateDoesNotExist:
                pass

        raise TemplateDoesNotExist(name)

    def load_template(self, template_name, template_dirs=None):
        key = template_name
        if template_dirs:
            key = ('-').join([template_name, hashlib.sha1(force_bytes(('|').join(template_dirs))).hexdigest()])
        if key not in self.template_cache:
            template, origin = self.find_template(template_name, template_dirs)
            if not hasattr(template, 'render'):
                try:
                    template = get_template_from_string(template, origin, template_name)
                except TemplateDoesNotExist:
                    return (
                     template, origin)

            self.template_cache[key] = template
        return (
         self.template_cache[key], None)

    def reset(self):
        """Empty the template cache."""
        self.template_cache.clear()