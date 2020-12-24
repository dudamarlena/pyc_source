# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craiglabenz/Sites/tablets/tablets/backend.py
# Compiled at: 2016-10-06 08:49:55
# Size of source mod 2**32: 487 bytes
from django.template.backends.base import BaseEngine
from django.template.exceptions import TemplateDoesNotExist
from tablets.models import Template

class TabletBackend(BaseEngine):

    def get_template(self, template_name):
        try:
            template = Template.objects.get(name=template_name)
        except Template.DoesNotExist as e:
            raise TemplateDoesNotExist(e.args, backend=self)
        else:
            return template.as_template()