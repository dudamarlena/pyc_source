# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erik/src/django/swida/source/permissions_widget/admin.py
# Compiled at: 2017-04-15 05:32:58
# Size of source mod 2**32: 1589 bytes
"""
Patch User and/or Group admin form to use the permission widget depending on
settings.

The patch works like this:

- get the user or group model,
- get the registered ModelAdmin from `admin.site` for this model,
- get the form of this ModelAdmin,
- inherit from the form and replace the permissions field,
- inherit from the modeladmin and replace the form,
- unregister the model admin,
- register the new inheriting model admin using the inheriting form with the
  permissions field override.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import admin
from .forms import PermissionSelectMultipleField
from . import settings
if settings.PATCH_USERADMIN:
    User = get_user_model()
    OriginalUserAdmin = admin.site._registry[User].__class__
    OriginalUserChangeForm = OriginalUserAdmin.form

    class NewUserChangeForm(OriginalUserChangeForm):
        user_permissions = PermissionSelectMultipleField(required=False)


    class NewUserAdmin(OriginalUserAdmin):
        form = NewUserChangeForm


    admin.site.unregister(User)
    admin.site.register(User, NewUserAdmin)
if settings.PATCH_GROUPADMIN:
    OriginalGroupAdmin = admin.site._registry[Group].__class__
    OriginalGroupChangeForm = OriginalGroupAdmin.form

    class NewGroupChangeForm(OriginalGroupChangeForm):
        permissions = PermissionSelectMultipleField(required=False)


    class NewGroupAdmin(OriginalGroupAdmin):
        form = NewGroupChangeForm


    admin.site.unregister(Group)
    admin.site.register(Group, NewGroupAdmin)