# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/template/loaders/locmem.py
# Compiled at: 2019-02-14 00:35:17
"""
Wrapper for loading templates from a plain Python dict.
"""
import warnings
from django.template import Origin, TemplateDoesNotExist
from django.utils.deprecation import RemovedInDjango20Warning
from .base import Loader as BaseLoader

class Loader(BaseLoader):

    def __init__(self, engine, templates_dict):
        self.templates_dict = templates_dict
        super(Loader, self).__init__(engine)

    def get_contents(self, origin):
        try:
            return self.templates_dict[origin.name]
        except KeyError:
            raise TemplateDoesNotExist(origin)

    def get_template_sources(self, template_name):
        yield Origin(name=template_name, template_name=template_name, loader=self)

    def load_template_source(self, template_name, template_dirs=None):
        warnings.warn('The load_template_sources() method is deprecated. Use get_template() or get_contents() instead.', RemovedInDjango20Warning)
        try:
            return (self.templates_dict[template_name], template_name)
        except KeyError:
            raise TemplateDoesNotExist(template_name)