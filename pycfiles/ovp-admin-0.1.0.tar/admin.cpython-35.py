# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-admin/ovp_admin/admin.py
# Compiled at: 2017-01-10 11:12:37
# Size of source mod 2**32: 1448 bytes
from django.contrib import admin
from ovp_admin.modules import *
import ovp_users.models as user, ovp_projects.models as project, ovp_organizations.models as organization
adm_reg = admin.site._registry
adm_reg[user.User].display_on_main_menu = True
adm_reg[project.Project].display_on_main_menu = True
adm_reg[project.Apply].display_on_main_menu = True
adm_reg[organization.Organization].display_on_main_menu = True