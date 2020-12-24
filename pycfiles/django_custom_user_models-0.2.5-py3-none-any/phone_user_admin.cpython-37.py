# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\admin\phone_user_admin.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 2139 bytes
import django.contrib.auth.admin as BaseUserAdmin
import django.utils.translation as _
from CustomAuth.forms import PhoneUserCreationForm, PhoneUserChangeForm
from phonenumber_field import widgets, modelfields

class PhoneUserAdmin(BaseUserAdmin):
    form = PhoneUserChangeForm
    add_form = PhoneUserCreationForm
    formfield_overrides = {modelfields.PhoneNumberField: {'widget': widgets.PhoneNumberPrefixWidget}}
    fieldsets = (
     (
      None,
      {'fields': ('username', 'password')}),
     (
      _('Personal info'),
      {'fields': ('first_name', 'last_name', 'cellphone', 'email')}),
     (
      _('finance'),
      {'fields': ('wallet', )}),
     (
      _('Permissions'),
      {'fields': ('is_active', 'is_verify', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
     (
      _('Important dates'),
      {'fields': ('date_verify', 'last_login')}))
    add_fieldsets = (
     (
      None,
      {'classes':('wide', ), 
       'fields':('cellphone', 'password1', 'password2')}),)
    list_display = ('cellphone', 'first_name', 'last_name', 'email', 'is_verify')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_verify')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'cellphone')
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions')