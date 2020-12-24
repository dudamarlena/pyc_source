# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/admin.py
# Compiled at: 2018-12-20 02:32:17
# Size of source mod 2**32: 968 bytes
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
csrf_protect_m = method_decorator(csrf_protect)

class PreferencesAdmin(admin.ModelAdmin):

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        If we only have a single preference object redirect to it,
        otherwise display listing.
        """
        model = self.model
        if model.objects.all().count() > 1:
            return super(PreferencesAdmin, self).changelist_view(request)
        else:
            obj = model.singleton.get()
            return redirect(reverse(('admin:%s_%s_change' % (
             model._meta.app_label, model._meta.model_name)),
              args=(
             obj.id,)))