# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/user_permissions.py
# Compiled at: 2020-03-01 01:12:07
# Size of source mod 2**32: 6738 bytes
"""
This python script will return the user's permission level for ANY given permission
"""
import json
from .models import *
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse

def return_user_permission_level(request, group_list, permission_field):
    """

    :param request:
    :param group: limits data to a certain group - Null if no group
    :param permission_field: which permission field we will be looking at. The available list is;
        permission_set_id
        permission_set_name
        administration_assign_users_to_group
        administration_create_group
        administration_create_permission_sets
        administration_create_users
        assign_campus_to_customer
        associate_project_and_tasks
        customer
        invoice
        invoice_product
        opportunity
        organisation
        organisation_campus
        project
        quote
        request_for_change
        requirement
        requirement_link
        task
        document
        contact_history
        project_history
        task_history
        whiteboard

        Please note - if you want to look up more than ONE permission, please include them in [] brackets. For example if
        you would like to look up; project, project_history, and document, then you would use ['project','project_history','document']
    :param min_permission_level: tells us what is the minimum level the user has to be, if they do not meet this requirement
        then the system will formward them onto the permission denied page. Default is 1 (read only)
    :return:
    """
    if not isinstance(permission_field, list):
        permission_field = [
         permission_field]
    user_permission_level = {}
    if request.user.is_superuser == True:
        for row in permission_field:
            user_permission_level[row] = 4

        user_permission_level['new_item'] = 4
        user_permission_level['administration'] = 4
        return user_permission_level
    for row in permission_field:
        if row == '':
            break
        if group_list == None:
            user_groups_results = user_group.objects.filter(is_deleted='FALSE',
              username=(request.user),
              permission_set__is_deleted='FALSE').aggregate(Max('permission_set__' + row))
            user_permission_level[row] = user_groups_results[('permission_set__' + row + '__max')]
        else:
            group_permission = 0
            for group_id in group_list:
                try:
                    user_groups_results = user_group.objects.filter(is_deleted='FALSE',
                      username=(request.user),
                      permission_set__is_deleted='FALSE',
                      group_id=(group_id['group_id'])).aggregate(Max('permission_set__' + row))
                except:
                    user_groups_results = user_group.objects.filter(is_deleted='FALSE',
                      username=(request.user),
                      permission_set__is_deleted='FALSE',
                      group_id=(group_id['group_id_id'])).aggregate(Max('permission_set__' + row))

                if user_groups_results[('permission_set__' + row + '__max')] == None or group_permission < user_groups_results[('permission_set__' + row + '__max')]:
                    group_permission = user_groups_results[('permission_set__' + row + '__max')]

            user_permission_level[row] = group_permission

    permission_results = user_group.objects.filter(is_deleted='FALSE',
      username=(request.user),
      permission_set__is_deleted='FALSE').aggregate(Max('permission_set__project'), Max('permission_set__task'), Max('permission_set__requirement'), Max('permission_set__request_for_change'), Max('permission_set__organisation'), Max('permission_set__customer'), Max('permission_set__administration_assign_user_to_group'), Max('permission_set__administration_create_group'), Max('permission_set__administration_create_permission_set'), Max('permission_set__administration_create_user'))
    user_permission_level['new_item'] = max(permission_results['permission_set__project__max'], permission_results['permission_set__task__max'], permission_results['permission_set__requirement__max'], permission_results['permission_set__organisation__max'], permission_results['permission_set__customer__max'])
    user_permission_level['administration'] = max(permission_results['permission_set__administration_assign_user_to_group__max'], permission_results['permission_set__administration_create_group__max'], permission_results['permission_set__administration_create_permission_set__max'], permission_results['permission_set__administration_create_user__max'])
    return user_permission_level