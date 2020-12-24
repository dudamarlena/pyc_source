# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-project-settings/project_settings/admin.py
# Compiled at: 2014-10-10 05:53:53
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from .models import Setting
from project_settings.forms import SettingsForm
from project_settings.registry import registry
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.contrib.messages import info

def admin_url(model, url, object_id=None):
    """
    Returns the URL for the given model and admin url name.
    """
    opts = model._meta
    url = 'admin:%s_%s_%s' % (opts.app_label, opts.object_name.lower(), url)
    args = ()
    if object_id is not None:
        args = (
         object_id,)
    return reverse(url, args=args)


class SettingAdmin(admin.ModelAdmin):
    change_list_template = 'admin/project_settings/setting/change_list.html'

    def changelist_redirect(self):
        changelist_url = admin_url(Setting, 'changelist')
        return HttpResponseRedirect(changelist_url)

    def add_view(self, *args, **kwargs):
        return self.changelist_redirect()

    def change_view(self, *args, **kwargs):
        return self.changelist_redirect()

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        settings_form = SettingsForm(request.POST or None)
        if settings_form.is_valid():
            settings_form.save()
            info(request, _('Settings were successfully updated.'))
            return self.changelist_redirect()
        else:
            extra_context['settings_form'] = settings_form
            extra_context['title'] = '%s %s' % (
             _('Change'), force_text(Setting._meta.verbose_name_plural))
            return super(SettingAdmin, self).changelist_view(request, extra_context)


admin.site.register(Setting, SettingAdmin)