# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/basic/admin.py
# Compiled at: 2018-03-27 09:45:07
# Size of source mod 2**32: 960 bytes
from __future__ import unicode_literals
from django.conf import settings

class LanguageTabsMixin(object):
    change_form_template = 'admin/djangocms_misc/modeltranslation_lang_tabs_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = extra_context or {}
        context['tab_languages'] = settings.LANGUAGES
        return super(LanguageTabsMixin, self).change_view(request,
          object_id=object_id,
          form_url=form_url,
          extra_context=context)

    def add_view(self, request, form_url='', extra_context=None):
        context = extra_context or {}
        context['tab_languages'] = settings.LANGUAGES
        return super(LanguageTabsMixin, self).add_view(request,
          form_url=form_url,
          extra_context=context)