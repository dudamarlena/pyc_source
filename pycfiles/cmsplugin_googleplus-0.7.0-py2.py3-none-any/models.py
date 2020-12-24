# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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