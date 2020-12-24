# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/zarinpals/admin.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from aparnik.contrib.users.admin import get_update_at
from .models import Bank

def get_payment(obj):
    return obj.payment.uuid


class BankAdmin(admin.ModelAdmin):
    list_display = (
     b'status', b'authority_id', b'ref_id', get_payment, get_update_at)
    actions = None

    class Meta:
        model = Bank

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True

    def change_view(self, request, object_id, form_url=b'', extra_context=None):
        """ customize edit form """
        extra_context = extra_context or {}
        extra_context[b'show_save_and_continue'] = False
        extra_context[b'show_save'] = False
        extra_context[b'show_save_and_add_another'] = False
        return super(BankAdmin, self).change_view(request, object_id, extra_context=extra_context)


admin.site.register(Bank, BankAdmin)