# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cmsplugin_googleform/models.py
# Compiled at: 2012-06-05 11:09:10
from django.db import models
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin

class GoogleFormsPlugin(CMSPlugin):
    form_id = models.CharField(_('form key'), max_length=64)
    height = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)

    @property
    def render_template(self):
        return select_template([
         'cms/plugins/googleform/%s-form.html' % (self.placeholder.slot.lower(),),
         'cms/plugins/googleform/form.html'])