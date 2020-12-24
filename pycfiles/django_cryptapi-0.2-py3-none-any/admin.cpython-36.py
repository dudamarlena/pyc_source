# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/admin.py
# Compiled at: 2018-11-13 04:54:27
# Size of source mod 2**32: 1728 bytes
from django.contrib import admin
from cryptapi.models import Provider, Request, Payment, RequestLog, PaymentLog

class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + [field.name for field in obj._meta.fields] + [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProviderAdmin(admin.ModelAdmin):
    add_fieldsets = (
     (
      'Coin',
      {'fields':('coin', ), 
       'description':'Select provider coin'}),
     (
      'Cold Wallet',
      {'fields':('cold_wallet', ), 
       'description':"Insert your cold wallet's address"}),
     (
      'Active',
      {'fields':('active', ), 
       'description':'Enable this provider'}))
    fieldsets = (
     (
      'Coin',
      {'fields':('coin', ), 
       'description':'Select provider coin'}),
     (
      'Cold Wallet',
      {'fields':('cold_wallet', ), 
       'description':"Insert your cold wallet's address"}),
     (
      'Active',
      {'fields':(('active',), ('last_updated',)), 
       'description':'Enable this provider'}))
    readonly_fields = ('last_updated', )


admin.site.register(Provider)
admin.site.register(Request, ReadOnlyAdmin)
admin.site.register(RequestLog, ReadOnlyAdmin)
admin.site.register(Payment, ReadOnlyAdmin)
admin.site.register(PaymentLog, ReadOnlyAdmin)