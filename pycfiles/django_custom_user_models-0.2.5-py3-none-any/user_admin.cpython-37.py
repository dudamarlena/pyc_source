# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\admin\user_admin.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 1886 bytes
import django.contrib.auth.admin as BaseUserAdmin
import django.utils.translation as _
from CustomAuth.forms.user_forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
     (
      None,
      {'fields': ('username', 'password')}),
     (
      _('Personal info'),
      {'fields': ('first_name', 'last_name', 'email')}),
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
       'fields':('email', 'password1', 'password2')}),)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_verify')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_verify')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'groups')
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions')