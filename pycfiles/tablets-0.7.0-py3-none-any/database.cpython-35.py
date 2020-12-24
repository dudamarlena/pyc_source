# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craiglabenz/Sites/tablets/tablets/loaders/database.py
# Compiled at: 2016-10-06 12:07:46
# Size of source mod 2**32: 746 bytes
from __future__ import unicode_literals
from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader
from tablets.models import Template

class Loader(Loader):
    is_usable = True

    def __call__(self, template_name, template_dirs=None):
        return self.load_template(template_name, template_dirs)

    def load_template(self, template_name, template_dirs=None):
        """
        Wraps the Django or Jinja2 template loading particulars
        """
        try:
            template = Template.objects.get(name=template_name)
            return (template.as_template(), template_name)
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)