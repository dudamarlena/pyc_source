# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/management/commands/set_group_perms.py
# Compiled at: 2018-05-17 05:02:04
__author__ = 'zhangyue'
import os, datetime, urllib2, json, time
from django.core.management.base import BaseCommand, CommandError
from django.db.models.signals import post_save
from django.db import transaction
from django.contrib.auth.models import User, Group, Permission
from bee_django_user.models import UserProfile, create_user

class Command(BaseCommand):
    help = 'set group permissions'
    permission_list = [
     {'group_name': '管理员', 
        'perms': [
                'can_manage', 'can_change_user_group', 'view_all_users',
                'view_all_classes']},
     {'group_name': '老师', 
        'perms': []},
     {'group_name': '客服', 
        'perms': []},
     {'group_name': '助教', 
        'perms': [
                'can_manage', 'view_teach_users',
                'view_teach_classes']}]

    @transaction.atomic
    def handle(self, *args, **options):
        groups = Group.objects.all()
        for group in groups:
            print group.name
            print type(group.name)
            for perm_dict in self.permission_list:
                print perm_dict['group_name']
                print type(perm_dict['group_name'])
                if group.name == perm_dict['group_name']:
                    perms = Permission.objects.filter(codename__in=perm_dict['perms'])
                    group.permissions = perms
                    break