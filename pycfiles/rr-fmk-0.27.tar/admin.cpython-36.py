# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/00P/01-dajngo/3d/app/rr/usuarios/admin.py
# Compiled at: 2018-04-05 10:03:25
# Size of source mod 2**32: 578 bytes
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from rr.usuarios.models import Cliente

class EmployeeInline(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'Clientes'


class UserAdmin(BaseUserAdmin):
    inlines = (
     EmployeeInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)