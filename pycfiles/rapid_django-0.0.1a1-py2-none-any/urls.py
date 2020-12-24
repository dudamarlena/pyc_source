# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/urls.py
# Compiled at: 2015-09-04 12:13:45
__author__ = 'marcos.medeiros'
from django.contrib.auth.models import User
from rapid.registry import Action
from rapid.models import Application, Profile
from rapid.forms import ManageUsers
from rapid import register
from rapid import permissions

def _can_manage_users(request):
    if not request.user.is_authenticated:
        return []
    p = []
    for a in request.user.managed_applications.all():
        p.extend(a.profile_set.all())

    return p


_manage_users_permistion = permissions.Permission(lambda r: False, _can_manage_users)
urlpatterns = register.model(Application, write_set=permissions.to_superusers(), read_set=permissions.to_all()) + register.model(Profile, write_set=permissions.to_superusers(), read_set=permissions.to_staff()) + register.instance_form(Profile, 'manage_users', 'Gerenciar Usuários', ManageUsers, _manage_users_permistion, icon='fa-users', visibility=Action.Visibility.list) + register.select(User, ['username'], permissions.to_staff(), 'usuario')