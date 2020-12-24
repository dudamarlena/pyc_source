# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact-setup/easy_contact_setup/admin.py
# Compiled at: 2014-10-23 11:29:40
from models import Setup
from django.contrib import admin
from forms import SetupForm
from django.utils.translation import ugettext_lazy as _

class SetupAdmin(admin.ModelAdmin):
    list_display = ('slug', 'active')
    fieldsets = (
     (
      _('Settings'),
      {'fields': ('active', 'slug', 'mail_to')}),
     (
      _('Optional settings - custom smtp server setup'),
      {'classes': ('collapse', ), 
         'fields': ('mail_host', 'mail_host_user', 'mail_host_pass')}))
    form = SetupForm


admin.site.register(Setup, SetupAdmin)