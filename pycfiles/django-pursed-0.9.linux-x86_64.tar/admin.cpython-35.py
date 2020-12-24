# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/strip/.local/share/virtualenvs/django-pursed/lib/python3.5/site-packages/wallet/admin.py
# Compiled at: 2017-06-07 07:47:39
# Size of source mod 2**32: 520 bytes
from django.contrib import admin
from .models import Transaction, Wallet

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet_id', 'value', 'running_balance', 'created_at')
    raw_id_fields = ('wallet', )

    def get_walled_id(self, obj):
        return obj.id


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'current_balance', 'created_at')
    raw_id_fields = ('user', )


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)