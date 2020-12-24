# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kubus/workspace/django-dbtemplate/dbtemplate/loader.py
# Compiled at: 2015-06-08 01:34:17
from django.template import TemplateDoesNotExist
from dbtemplate.models import Template
try:
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:
    from django.template.loader import BaseLoader

class DatabaseLoader(BaseLoader):
    """
    A custom template loader to load templates from the database.
    """
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            template = Template.objects.get(slug=template_name)
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)

        return (
         template.data, 'dbtemplate:%s' % template_name)