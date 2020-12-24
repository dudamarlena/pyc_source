# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_postfix/admin.py
# Compiled at: 2012-06-04 12:02:54
from django.contrib import admin
from django_postfix.models import Domain, Mailbox, Alias

class AliasInline(admin.TabularInline):
    model = Alias
    exclude = ['domain']
    extra = 0


class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'active', 'aliases', 'mailboxes', 'backupmx')
    search_fields = ('domain', 'description')


class MailboxAdmin(admin.ModelAdmin):
    search_fields = ('username', )
    list_display = ('username', 'maildir', 'quote')
    list_filter = ('domain', )
    date_hierarchy = 'created'
    inlines = [AliasInline]


admin.site.register(Domain, DomainAdmin)
admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Alias)