# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/PACKAGES/WORKON/workon/views/template.py
# Compiled at: 2018-05-07 05:46:52
# Size of source mod 2**32: 653 bytes
from django.views import generic
__all__ = [
 'Template']

class Template(generic.TemplateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return getattr(self, 'ajax_template_name', getattr(self, 'template_name_ajax', getattr(self, 'xhr_template_name', getattr(self, 'template_name_xhr', getattr(self, 'template_name')))))
        else:
            return self.template_name