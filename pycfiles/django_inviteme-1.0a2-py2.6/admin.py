# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/inviteme/admin.py
# Compiled at: 2012-04-10 18:26:28
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from inviteme.models import ContactMail

class ContactMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip_address', 'submit_date')
    fieldsets = (
     (
      None, {'fields': ('site', )}),
     (
      _('Content'), {'fields': ('email', 'submit_date', 'ip_address')}))
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date', )


admin.site.register(ContactMail, ContactMailAdmin)