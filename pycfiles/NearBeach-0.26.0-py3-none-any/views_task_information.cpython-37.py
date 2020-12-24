# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/views_task_information.py
# Compiled at: 2020-03-27 20:27:19
# Size of source mod 2**32: 4419 bytes
"""
VIEWS - task information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the TASK INFORMATION MODULES. This is to help keep the VIEWS
file clean from AJAX (spray and wipe).
"""
from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from .user_permissions import return_user_permission_level

@login_required(login_url='login', redirect_field_name='')
def information_task_delete_assigned_users(request, task_id, user_id):
    assigned_users_save = assigned_user.objects.filter(task_id=task_id,
      user_id=user_id)
    assigned_users_save.update(is_deleted='TRUE')
    t = loader.get_template('NearBeach/blank.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def information_task_customer(request, task_id):
    task_groups_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id).values('group_id')
    permission_results = return_user_permission_level(request, task_groups_results, 'task')
    if request.method == 'POST':
        customer_id = int(request.POST.get('add_customer_select'))
        submit_customer = task_customer(task_id=task.objects.get(pk=task_id),
          customer_id=customer.objects.get(pk=customer_id),
          change_user=(request.user))
        submit_customer.save()
    task_results = task.objects.get(task_id=task_id)
    new_customers_results = customer.objects.filter(organisation_id=(task_results.organisation_id.organisation_id),
      is_deleted='FALSE').exclude(customer_id__in=(task_customer.objects.filter(is_deleted='FALSE',
      task_id=(task_results.task_id)).values('customer_id')))
    task_customers_results = task_customer.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    t = loader.get_template('NearBeach/task_information/task_customers.html')
    c = {'task_results':task_results, 
     'new_customers_results':new_customers_results, 
     'task_customers_results':task_customers_results, 
     'task_permissions':permission_results['task']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def information_task_history(request, task_id):
    task_groups_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task.objects.get(task_id=task_id)).values('group_id_id')
    permission_results = return_user_permission_level(request, task_groups_results, ['task', 'task_history'])
    if request.method == 'POST':
        form = information_task_history_form(request.POST, request.FILES)
        if form.is_valid():
            task_history_results = form.cleaned_data['task_history']
            if not task_history_results == '':
                current_user = request.user
                task_id_connection = task.objects.get(task_id=task_id)
                data = task_history(task_id=task_id_connection,
                  user_id=current_user,
                  task_history=task_history_results,
                  user_infomation=(current_user.id),
                  change_user=(request.user))
                data.save()
    task_history_results = task_history.objects.filter(task_id=task_id,
      is_deleted='FALSE')
    t = loader.get_template('NearBeach/task_information/task_history.html')
    c = {'task_history_results':task_history_results, 
     'task_permissions':permission_results['task'], 
     'task_history_permissions':permission_results['task_history']}
    return HttpResponse(t.render(c, request))