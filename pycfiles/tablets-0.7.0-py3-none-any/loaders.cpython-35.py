# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craiglabenz/Sites/tablets/tablets/j2/loaders.py
# Compiled at: 2016-10-06 12:21:13
# Size of source mod 2**32: 1479 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.template.loaders.base import Loader
from django.template.utils import get_app_template_dirs
from django.utils import six
from jinja2.exceptions import TemplateNotFound
from tablets.j2.exceptions import Jinja2NotInstalled
try:
    import jinja2
    from jinja2.loaders import BaseLoader
except ImportError as e:
    jinja2 = None

class DatabaseLoader(BaseLoader):
    __doc__ = '\n    This guy talks to the database and returns something Jinja2 wants.\n    '

    def __init__(self, encoding='utf-8', should_reload_db_templates=True):
        self.encoding = encoding
        self.should_reload_db_templates = should_reload_db_templates

    def uptodate(self):
        return not self.should_reload_db_templates

    def get_source(self, environment, template):
        if not jinja2:
            raise Jinja2NotInstalled
        from tablets.models import Template
        try:
            tmpl = Template.objects.get(name=template, template_engine=Template.JINJA2)
            content = tmpl.get_content()
            if hasattr(content, 'decode'):
                content = content.decode(self.encoding)
            return (content, template, self.uptodate)
        except Template.DoesNotExist:
            raise TemplateNotFound(template)