# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/email_filter/admin.py
# Compiled at: 2014-03-25 06:56:15
from django.contrib import admin
from email_filter.models import EmailLog, EmailRedirect, EmailAttachment

class EmailAttachmentInline(admin.TabularInline):
    model = EmailAttachment


class EmailLogAdmin(admin.ModelAdmin):
    list_display = [
     'sender', 'recipient', 'subject', 'created']
    search_fields = ['sender', 'recipient', 'subject']
    list_filter = ['created']
    inlines = [EmailAttachmentInline]


admin.site.register(EmailLog, EmailLogAdmin)
admin.site.register(EmailAttachment)
admin.site.register(EmailRedirect, admin.ModelAdmin)