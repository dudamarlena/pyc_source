# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/views.py
# Compiled at: 2020-04-05 05:09:39
# Size of source mod 2**32: 397536 bytes
from .forms import *
from .models import *
from .private_media import *
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Q, Min, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.urls import reverse
from .misc_functions import *
from .user_permissions import return_user_permission_level
from datetime import timedelta
from django.db.models import Max
from django.core.mail import EmailMessage, EmailMultiAlternatives
from geolocation.main import GoogleMaps
from django.http import JsonResponse
from urllib.request import urlopen
from weasyprint import HTML
from django.core.mail import send_mail
from urllib.parse import urlparse, urlencode, quote_plus
from docx import Document
from docx.shared import Cm, Inches
from bs4 import BeautifulSoup
from .models import RFC_APPROVAL, RFC_IMPACT, RFC_PRIORITY, RFC_RISK, RFC_STATUS, RFC_TYPE
import datetime, json, simplejson, urllib.parse, pypandoc, requests, random, time

@login_required(login_url='login', redirect_field_name='')
def add_campus_to_customer(request, customer_id, campus_id):
    """
    This function can only exist in POST. It will add a customer to a campus
    :param request:
    :param customer_id: the customer's id
    :param campus_id: the campus's id to add the customer too
    :return: Success or fail - depending if it worked or not
    """
    if request.method == 'POST':
        customer_instance = customer.objects.get(customer_id=customer_id)
        campus_instances = campus.objects.get(campus_id=campus_id)
        submit_campus = customer_campus(customer_id=customer_instance,
          campus_id=campus_instances,
          customer_phone='',
          customer_fax='',
          change_user=(request.user))
        submit_campus.save()
        response_data = {}
        response_data['customer_campus_id'] = submit_campus.customer_campus_id
        return JsonResponse({'customer_campus_id': submit_campus.customer_campus_id})
    return HttpResponseBadRequest('Sorry, you can only do this in post.')


@login_required(login_url='login', redirect_field_name='')
def admin_group(request, location_id, destination):
    t = loader.get_template('NearBeach/administration/admin_group.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def admin_permission_set(request, group_id):
    """
    Admin permission set will render a list of all permission set's connected to the current group. This admin def
    is only appliciable for the group functionality at the moment. Hence it only contains a "Group ID" as input

    If this is rendering for the group - it will allow users to add more permission sets to the group
    :param request:
    :param group_id: the primary key for the group
    :return: A rendered list of permissions

    Method
    ~~~~~~
    1. Check the user permissions
    2. If post - go through post. Check comments here
    3. Get data for permission sets connected to this group
    4. Render the template :) and return results to user
    """
    permission_results = return_user_permission_level(request, [None], ['administration_create_group'])
    if permission_results['administration_create_group'] <= 1:
        return HttpResponseRedirect(reverse(permission_denied))
        if request.method == 'POST' and permission_results['administration_create_group'] >= 3:
            form = add_permission_set_to_group_form((request.POST),
              group_id=group_id)
            if form.is_valid():
                group_permission_submit = group_permission(group_id=group_id,
                  permission_set=(form.cleaned_data['add_permission_set']),
                  change_user=(request.user))
                group_permission_submit.save()
    else:
        print(form.errors)
    permission_set_results = group_permission.objects.filter(is_deleted='FALSE',
      group_id=group_id)
    t = loader.get_template('NearBeach/administration/admin_permission_set.html')
    c = {'permission_set_results':permission_set_results, 
     'group_id':group_id, 
     'add_permission_set_to_group_form':add_permission_set_to_group_form(group_id=group_id), 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def admin_add_user(request, group_id):
    """
    Pulls up a list of users for the group information. This def shows a list and grants you the ability to add new users
    to a group.

    Please note - as a user can have multiple permission sets per group, it does not restrict duplications.
    :param request:
    :param group_id: The group ID we are looking at
    :return: HTML

    Method
    ~~~~~~
    1. Check permissions
    2. If post - do post method - more comments here
    3. Obtain information like users already assigned to the group
    4. Render webpage
    """
    permission_results = return_user_permission_level(request, [None], ['administration_create_group'])
    if permission_results['administration_create_group'] <= 1:
        return HttpResponseRedirect(reverse(permission_denied))
        if request.method == 'POST':
            form = add_user_to_group_form((request.POST),
              group_id=group_id)
            if form.is_valid():
                user_group_submit = user_group(username=(form.cleaned_data['add_user']),
                  group=group.objects.get(group_id=group_id),
                  permission_set=(form.cleaned_data['permission_set']),
                  change_user=(request.user))
                user_group_submit.save()
    else:
        print(form.errors)
    user_group_results = user_group.objects.filter(is_deleted='FALSE',
      group_id=group_id)
    t = loader.get_template('NearBeach/administration/admin_user.html')
    c = {'add_user_to_group_form':add_user_to_group_form(group_id=group_id), 
     'administration_permission':permission_results['administration'], 
     'user_group_results':user_group_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def alerts(request):
    """
    Alerts are shown after the user logs in with any outstanding objects, i.e. Projects that have end dates in the past.
    :param request:
    :return: Returns a web page of alerts

    Method
    ~~~~~~
    1. get the compare date, that is 24 hours into the future.
    2. filter projects, tasks, opportunity, and quotes. The filters will be if they are still active (not completed or resolved)
        and if the end date is less than or equal to the campare time.
    3. If there are no results for any of the objects - redirect to dashboard
    4. Loaad the alerts page.
    """
    compare_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    project_results = project.objects.filter(is_deleted='FALSE',
      project_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      project_id__isnull=False,
      assigned_user=(request.user)).values('project_id')),
      project_end_date__lte=compare_time,
      project_status__in={
     'Backlog', 'Blocked', 'In Progress', 'Test/Review'})
    task_results = task.objects.filter(is_deleted='FALSE',
      task_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      task_id__isnull=False,
      assigned_user=(request.user)).values('task_id')),
      task_end_date__lte=compare_time,
      task_status__in={
     'Backlog', 'Blocked', 'In Progress', 'Test/Review'})
    opportunity_results = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      assigned_user=(request.user)).values('opportunity_id')),
      opportunity_expected_close_date__lte=compare_time,
      opportunity_stage_id__in=(list_of_opportunity_stage.objects.filter(opportunity_closed='FALSE').values('opportunity_stage_id')))
    quote_results = quote.objects.filter(is_deleted='FALSE',
      quote_stage_id__in=(list_of_quote_stage.objects.filter(quote_closed='FALSE').values('quote_stage_id')),
      quote_valid_till__lte=compare_time)
    if not project_results:
        if not task_results:
            if not opportunity_results:
                if not quote_results:
                    return HttpResponseRedirect(reverse('dashboard'))
    t = loader.get_template('NearBeach/alerts.html')
    c = {'project_results':project_results, 
     'task_results':task_results, 
     'opportunity_results':opportunity_results, 
     'quote_results':quote_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def assign_customer_project_task(request, customer_id):
    """
    This allows the user to allocate multiple projects/tasks to a customer in a single search.
    :param request:
    :param customer_id: The customer's id
    :return: Redirect to the customer's information page

    Method
    ~~~~~~
    1. Check current users permission - are they allowed to do this. If not, send them away
    2. If request is post - create a new row for each project/tasks assigned to the user (read comments in section)
    3. If request is not post - get project/task/customer infromation
    4. Render the page
    """
    user_group_results = user_group.objects.filter(is_deleted='FALSE',
      username=(request.user.id)).values('group_id')
    permission_results = return_user_permission_level(request, user_group_results, ['task', 'project'])
    if permission_results['task'] <= 1 or permission_results['project'] <= 1:
        return HttpResponseRedirect(reverse(permission_denied))
    if request.POST:
        assign_projects = request.POST.getlist('project_checkbox')
        assign_task = request.POST.getlist('task_checkbox')
        customer_instance = customer.objects.get(customer_id=customer_id)
        for row in assign_projects:
            project_instance = project.objects.get(project_id=row)
            project_customer_submit = project_customer(project_id=project_instance,
              customer_id=customer_instance,
              change_user=(request.user))
            if not project_customer_submit.save():
                print('Error saving')

        for row in assign_task:
            task_instance = task.objects.get(task_id=row)
            task_customer_submit = task_customer(task_id=task_instance,
              customer_id=customer_instance,
              change_user=(request.user))
            task_customer_submit.save()

        return HttpResponseRedirect(reverse('customer_information', args={customer_id}))
    customer_results = customer.objects.get(customer_id=customer_id)
    project_results = project.objects.filter(is_deleted='FALSE',
      project_status__in=('Backlog', 'Blocked', 'In Progress', 'Test/Review'),
      project_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username_id=(request.user.id)).values('group_id'))).values('project_id')))
    task_results = task.objects.filter(is_deleted='FALSE',
      task_status__in=('Backlog', 'Blocked', 'In Progress', 'Test/Review'),
      task_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username_id=(request.user.id)).values('group_id'))).values('task_id')))
    t = loader.get_template('NearBeach/assign_customer_project_task.html')
    c = {'project_results':project_results, 
     'task_results':task_results, 
     'customer_results':customer_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def assigned_group_add(request, location_id, destination):
    """

    :param request:
    :param location_id:
    :param destination:
    :return:
    """
    if request.method == 'POST':
        form = assign_group_add_form((request.POST),
          location_id=location_id,
          destination=destination)
        if form.is_valid():
            if destination == 'project':
                object_assignment_submit = object_assignment(project_id=project.objects.get(project_id=location_id),
                  group_id=(form.cleaned_data['add_group']),
                  change_user=(request.user))
            else:
                if destination == 'task':
                    object_assignment_submit = object_assignment(task_id=task.objects.get(task_id=location_id),
                      group_id=(form.cleaned_data['add_group']),
                      change_user=(request.user))
                else:
                    if destination == 'requirement':
                        object_assignment_submit = object_assignment(requirement_id=requirement.objects.get(requirement_id=location_id),
                          group_id=(form.cleaned_data['add_group']),
                          change_user=(request.user))
                    else:
                        if destination == 'quote':
                            object_assignment_submit = object_assignment(quote_id=quote.objects.get(quote_id=location_id),
                              group_id=(form.cleaned_data['add_group']),
                              change_user=(request.user))
                        else:
                            if destination == 'kanban_board':
                                object_assignment_submit = object_assignment(kanban_board_id=kanban_board.objects.get(kanban_board_id=location_id),
                                  group_id=(form.cleaned_data['add_group']),
                                  change_user=(request.user))
                            else:
                                if destination == 'opportunity':
                                    object_assignment_submit = object_assignment(opportunity_id=opportunity.objects.get(opportunity_id=location_id),
                                      group_id=(form.cleaned_data['add_group']),
                                      change_user=(request.user))
                                else:
                                    if destination == 'request_for_change':
                                        object_assignment_submit = object_assignment(request_for_change=request_for_change.objects.get(rfc_id=location_id),
                                          group_id=(form.cleaned_data['add_group']),
                                          change_user=(request.user))
                                    object_assignment_submit.save()
        else:
            print(form.errors)
    t = loader.get_template('NearBeach/assigned_groups/assigned_groups_add.html')
    c = {'assign_group_add_form': assign_group_add_form(location_id=location_id,
                                destination=destination)}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def assigned_group_delete(request, object_assignment_id):
    """
    assigned group delete will delete an assigned group against an object. Please note this has to be through
    POST. This is a security measure
    """
    if request.method == 'POST':
        object_assignment_update = object_assignment.objects.get(object_assignment_id=object_assignment_id)
        object_assignment_update.is_deleted = 'TRUE'
        object_assignment_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Action can only be done through POST')


@login_required(login_url='login', redirect_field_name='')
def assigned_group_list(request, location_id, destination):
    if destination == 'project':
        group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
          project_id=location_id).exclude(group_id=None)
    else:
        if destination == 'task':
            group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
              task_id=location_id).exclude(group_id=None)
        else:
            if destination == 'requirement':
                group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
                  requirement_id=location_id).exclude(group_id=None)
            else:
                if destination == 'quote':
                    group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
                      quote_id=location_id).exclude(group_id=None)
                else:
                    if destination == 'kanban_board':
                        group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
                          kanban_board_id=location_id).exclude(group_id=None)
                    else:
                        if destination == 'opportunity':
                            group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
                              opportunity_id=location_id).exclude(group_id=None)
                        else:
                            if destination == 'requirement':
                                group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
                                  requirement_id=location_id).exclude(group_id=None)
                            else:
                                if destination == 'request_for_change':
                                    group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
                                      request_for_change=location_id).exclude(group_id=None)
                                else:
                                    group_list_results = ''
    t = loader.get_template('NearBeach/assigned_groups/assigned_groups_list.html')
    c = {'group_list_results':group_list_results, 
     'destination':destination}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def assigned_opportunity_connection_add(request, opportunity_id, destination):
    """
    We want the ability to add either an organisation or customer to an opportunity. This function will apply that.
    :param request:
    :param opportunity_id: The opportunity that we are assigning the connection to
    :param destination: If we are assigning a customer or organisation
    :return: Search Page

    Method
    ~~~~~~
    1. Check user's permissions - send them to the naughty corner if they do not have permission
    2. Check to see if the method is post - follow instructions here if it is post
    3. Check to see if the destination is customer or organisation. Pull out the relevant search results.
    4. Collect the template
    5. Render the results
    """
    permission_results = return_user_permission_level(request, None, 'opportunity')
    if permission_results['opportunity'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = connect_form(request.POST)
        if form.is_valid():
            customer_extract = form.cleaned_data['customers']
            organisation_extract = form.cleaned_data['organisations']
            for row in customer_extract:
                submit_object_assignment = object_assignment(opportunity_id=opportunity.objects.get(opportunity_id=opportunity_id),
                  customer=row,
                  change_user=(request.user))
                submit_object_assignment.save()

            for row in organisation_extract:
                submit_object_assignment = object_assignment(opportunity_id=opportunity.objects.get(opportunity_id=opportunity_id),
                  organisation=row,
                  change_user=(request.user))
                submit_object_assignment.save()

            return HttpResponseRedirect(reverse('opportunity_information', args={opportunity_id}))
        print('There was an issue getting data from the form. Sending user back.')
        print(form)
    elif destination == 'organisation':
        t = loader.get_template('NearBeach/opportunity_information/opportunity_connect_organisation.html')
    else:
        t = loader.get_template('NearBeach/opportunity_information/opportunity_connect_customer.html')
    c = {'connect_form':connect_form(), 
     'opportunity_id':opportunity_id, 
     'opportunity_permission':permission_results['opportunity'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def assigned_opportunity_connection_delete(request, opportunity_id, location_id, destination):
    """
    This will remove any organisation/customer connection to an opportunity.
    :param request:
    :param location_id: The ID of the customer/organisation
    :param destination: This tells the program if we are looking for an organisation or location.
    :return: Success results

    Method
    ~~~~~~
    1. Check permissions - send user away if they do not have permissions
    2. Check to make sure this is a POST
    3. Filter for the relivant organisation/customer connection
    4. Change the is_deleted value to TRUE
    5. Send back blank page
    """
    permission_results = return_user_permission_level(request, None, 'opportunity')
    if permission_results['opportunity'] != 4:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        if destination == 'organisation':
            object_assignment.objects.filter(is_deleted='FALSE',
              organisation_id=location_id,
              opportunity_id=opportunity_id).update(is_deleted='TRUE')
        else:
            object_assignment.objects.filter(is_deleted='FALSE',
              customer_id=location_id,
              opportunity_id=opportunity_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - can only do this request via post')


@login_required(login_url='login', redirect_field_name='')
def assigned_rfc_connection_add(request, rfc_id, destination):
    """
    We want the ability to add either an organisation or customer to an request for change. This function will apply that.
    :param request:
    :param rfc_id: The rfc that we are assigning the connection to
    :param destination: If we are assigning a customer or organisation
    :return: Search Page

    Method
    ~~~~~~
    1. Check user's permissions - send them to the naughty corner if they do not have permission
    2. Check to see if the method is post - follow instructions here if it is post
    3. Check to see if the destination is customer or organisation. Pull out the relevant search results.
    4. Collect the template
    5. Render the results
    """
    permission_results = return_user_permission_level(request, None, 'request_for_change')
    if permission_results['request_for_change'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = connect_form(request.POST)
        if form.is_valid():
            customer_extract = form.cleaned_data['customers']
            organisation_extract = form.cleaned_data['organisations']
            for row in customer_extract:
                submit_stakeholder = request_for_change_stakeholder(request_for_change=request_for_change.objects.get(rfc_id=rfc_id),
                  customer=row,
                  change_user=(request.user))
                submit_stakeholder.save()

            for row in organisation_extract:
                submit_stakeholder = request_for_change_stakeholder(request_for_change=request_for_change.objects.get(rfc_id=rfc_id),
                  organisation=row,
                  change_user=(request.user))
                submit_stakeholder.save()

            return HttpResponseRedirect(reverse('request_for_change_information', args={rfc_id}))
        print('There was an issue getting data from the form. Sending user back.')
        print(form)
    else:
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        if destination == 'organisation':
            t = loader.get_template('NearBeach/request_for_change/rfc_connect_organisation.html')
        else:
            t = loader.get_template('NearBeach/request_for_change/rfc_connect_customer.html')
    c = {'connect_form':connect_form(),  'rfc_id':rfc_id, 
     'rfc_results':rfc_results, 
     'rfc_permission':permission_results['request_for_change'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def assigned_rfc_connection_delete(request, rfc_id, location_id, destination):
    """
    This will remove any organisation/customer connection to an rfc.
    :param request:
    :param location_id: The ID of the customer/organisation
    :param destination: This tells the program if we are looking for an organisation or location.
    :return: Success results

    Method
    ~~~~~~
    1. Check permissions - send user away if they do not have permissions
    2. Check to make sure this is a POST
    3. Filter for the relevant organisation/customer connection
    4. Change the is_deleted value to TRUE
    5. Send back blank page
    """
    permission_results = return_user_permission_level(request, None, 'opportunity')
    if permission_results['opportunity'] != 4:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        if destination == 'organisation':
            request_for_change_stakeholder.objects.filter(is_deleted='FALSE',
              organisation_id=location_id,
              request_for_change=rfc_id).update(is_deleted='TRUE')
        else:
            request_for_change_stakeholder.objects.filter(is_deleted='FALSE',
              customer_id=location_id,
              request_for_change=rfc_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - can only do this request via post')


@login_required(login_url='login', redirect_field_name='')
def assigned_user_add(request, location_id, destination):
    """
    We want the ability for the User to grant permission to anyone. For example, if a group owns this requirement,
    however we need someone from a different group, i.e. IT, then we can assign them to this requirement as a
    permission and they should be able to access it.
    """
    if request.method == 'POST':
        form = assign_user_add_form((request.POST),
          location_id=location_id,
          destination=destination)
        if form.is_valid():
            if destination == 'project':
                object_assignment_submit = object_assignment(project_id=project.objects.get(project_id=location_id),
                  assigned_user=(form.cleaned_data['add_user']),
                  change_user=(request.user))
                object_assignment_submit.save()
            else:
                if destination == 'task':
                    object_assignment_submit = object_assignment(task_id=task.objects.get(task_id=location_id),
                      assigned_user=(form.cleaned_data['add_user']),
                      change_user=(request.user))
                    object_assignment_submit.save()
                else:
                    if destination == 'requirement':
                        object_assignment_submit = object_assignment(requirement_id=requirement.objects.get(requirement_id=location_id),
                          assigned_user=(form.cleaned_data['add_user']),
                          change_user=(request.user))
                        object_assignment_submit.save()
                    else:
                        if destination == 'quote':
                            object_assignment_submit = object_assignment(quote_id=quote.objects.get(quote_id=location_id),
                              assigned_user=(form.cleaned_data['add_user']),
                              change_user=(request.user))
                            object_assignment_submit.save()
                        else:
                            if destination == 'kanban_board':
                                object_assignment_submit = object_assignment(kanban_board_id=kanban_board.objects.get(kanban_board_id=location_id),
                                  assigned_user=(form.cleaned_data['add_user']),
                                  change_user=(request.user))
                                object_assignment_submit.save()
                            else:
                                if destination == 'opportunity':
                                    object_assignment_submit = object_assignment(opportunity_id=opportunity.objects.get(opportunity_id=location_id),
                                      assigned_user=(form.cleaned_data['add_user']),
                                      change_user=(request.user))
                                    object_assignment_submit.save()
        else:
            print(form.errors)
    t = loader.get_template('NearBeach/assigned_users/assigned_user_add.html')
    c = {'assign_user_add_form': assign_user_add_form(location_id=location_id,
                               destination=destination)}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def assigned_user_delete(request, object_assignment_id):
    if request.method == 'POST':
        object_assignment_update = object_assignment.objects.get(object_assignment_id=object_assignment_id)
        object_assignment_update.change_user = request.user
        object_assignment_update.is_deleted = 'TRUE'
        object_assignment_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - can only do this in POST')


@login_required(login_url='login', redirect_field_name='')
def assigned_user_list(request, location_id, destination):
    permission_results = return_user_permission_level(request, None, destination)
    if destination == 'project':
        assigned_user_results = object_assignment.objects.filter(is_deleted='FALSE',
          project_id=location_id).exclude(assigned_user=None)
    else:
        if destination == 'task':
            assigned_user_results = object_assignment.objects.filter(is_deleted='FALSE',
              task_id=location_id).exclude(assigned_user=None)
        else:
            if destination == 'requirement':
                assigned_user_results = object_assignment.objects.filter(is_deleted='FALSE',
                  requirement_id=location_id).exclude(assigned_user=None)
            else:
                if destination == 'quote':
                    assigned_user_results = object_assignment.objects.filter(is_deleted='FALSE',
                      quote_id=location_id).exclude(assigned_user=None)
                else:
                    if destination == 'opportunity':
                        assigned_user_results = object_assignment.objects.filter(is_deleted='FALSE',
                          opportunity_id=location_id).exclude(assigned_user=None)
                    else:
                        assigned_user_results = ''
    t = loader.get_template('NearBeach/assigned_users/assigned_user_list.html')
    c = {'assigned_user_results':assigned_user_results, 
     'permissions':permission_results[destination]}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def associate(request, project_id, task_id, project_or_task):
    submit_result = object_assignment(project_id_id=project_id,
      task_id_id=task_id,
      change_user=(request.user))
    submit_result.save()
    if project_or_task == 'P':
        return HttpResponseRedirect(reverse('project_information', args={project_id}))
    return HttpResponseRedirect(reverse('task_information', args={task_id}))


@login_required(login_url='login', redirect_field_name='')
def associated_projects(request, task_id):
    """
        We want the ability for the user to assign any project to the current
        task that their group owns. The user will have the ability to
        check to see if they want only new or open, or if they would like
        to see closed task too.
        """
    task_groups_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id).values('group_id_id')
    permission_results = return_user_permission_level(request, task_groups_results, ['task'])
    if permission_results['task'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    projects_results = project.objects.filter(is_deleted='FALSE',
      project_status__in={
     'Backlog', 'Blocked', 'In Progress', 'Test/Review'})
    t = loader.get_template('NearBeach/associated_project.html')
    c = {'projects_results':projects_results, 
     'task_id':task_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def associated_task(request, project_id):
    """
        We want the ability for the user to assign any task to the current
        project that their group owns. The user will have the ability to
        check to see if they want only new or open, or if they would like
        to see closed task too.
        """
    project_groups_results = object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project.objects.get(project_id=project_id)).values('group_id_id')
    permission_results = return_user_permission_level(request, project_groups_results, ['project'])
    if permission_results['project'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    task_results = task.objects.filter(is_deleted='FALSE',
      task_status__in=('Backlog', 'Blocked', 'In Progress', 'Test/Review'))
    t = loader.get_template('NearBeach/associated_task.html')
    c = {'task_results':task_results, 
     'project_id':project_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def bug_add(request, location_id, destination, bug_id, bug_client_id):
    if request.method == 'POST':
        bug_client_instance = bug_client.objects.get(bug_client_id=bug_client_id)
        url = '%s%sbug?id=%s' % (
         escape(bug_client_instance.bug_client_url),
         escape(bug_client_instance.list_of_bug_client.bug_client_api_url),
         escape(bug_id))
        if url.lower().startswith('http'):
            req = urllib.request.Request(url)
        else:
            raise ValueError from None
        with urllib.request.urlopen(req) as (response):
            json_data = json.load(response)
        bug_submit = bug(bug_client=bug_client_instance,
          bug_code=bug_id,
          bug_description=(str(json_data['bugs'][0]['summary'])),
          bug_status=(str(json_data['bugs'][0]['status'])),
          change_user=(request.user))
        if destination == 'project':
            bug_submit.project = project.objects.get(project_id=location_id)
        else:
            if destination == 'task':
                bug_submit.task = task.objects.get(task_id=location_id)
            else:
                bug_submit.requirement = requirement.objects.get(requirement_id=location_id)
        bug_submit.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Only POST requests allowed')


@login_required(login_url='login', redirect_field_name='')
def bug_client_delete(request, bug_client_id):
    permission_results = return_user_permission_level(request, None, 'bug_client')
    if request.method == 'POST':
        if permission_results['bug_client'] == 4:
            bug_client_update = bug_client.objects.get(bug_client_id=bug_client_id)
            bug_client_update.is_deleted = 'TRUE'
            bug_client_update.save()
            t = loader.get_template('NearBeach/blank.html')
            c = {}
            return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Only POST requests allowed')


@login_required(login_url='login', redirect_field_name='')
def bug_client_information(request, bug_client_id):
    permission_results = return_user_permission_level(request, None, 'bug_client')
    if permission_results['bug_client'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
        form_errors = ''
        if request.method == 'POST':
            form = bug_client_form(request.POST)
            if form.is_valid():
                bug_client_name = form.cleaned_data['bug_client_name']
                list_of_bug_client = form.cleaned_data['list_of_bug_client']
                bug_client_url = form.cleaned_data['bug_client_url']
                try:
                    url = bug_client_url + list_of_bug_client.bug_client_api_url + 'version'
                    if url.lower().startswith('http'):
                        req = urllib.request.Request(url)
                    else:
                        raise ValueError from None
                    with urllib.request.urlopen(req) as (response):
                        data = json.load(response)
                    bug_client_save = bug_client.objects.get(bug_client_id=bug_client_id)
                    bug_client_save.bug_client_name = bug_client_name
                    bug_client_save.list_of_bug_client = list_of_bug_client
                    bug_client_save.bug_client_url = bug_client_url
                    bug_client_save.change_user = request.user
                    bug_client_save.save()
                    return HttpResponseRedirect(reverse('bug_client_list'))
                except:
                    form_errors = 'Could not connect to the API'
                    print('There was an error')

    else:
        print(form.errors)
        form_errors(form.errors)
    bug_client_results = bug_client.objects.get(bug_client_id=bug_client_id)
    bug_client_initial = {'bug_client_name':bug_client_results.bug_client_name, 
     'list_of_bug_client':bug_client_results.list_of_bug_client, 
     'bug_client_url':bug_client_results.bug_client_url}
    t = loader.get_template('NearBeach/bug_client_information.html')
    c = {'bug_client_form':bug_client_form(initial=bug_client_initial), 
     'bug_client_id':bug_client_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'form_errors':form_errors}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def bug_client_list(request):
    permission_results = return_user_permission_level(request, None, 'bug_client')
    if permission_results['bug_client'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    bug_client_results = bug_client.objects.filter(is_deleted='FALSE')
    t = loader.get_template('NearBeach/bug_client_list.html')
    c = {'bug_client_results':bug_client_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'bug_client_permission':permission_results['bug_client']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def bug_list(request, location_id=None, destination=None):
    if destination == 'project':
        bug_results = bug.objects.filter(is_deleted='FALSE',
          project=location_id)
    else:
        if destination == 'task':
            bug_results = bug.objects.filter(is_deleted='FALSE',
              task=location_id)
        else:
            if destination == 'requirement':
                bug_results = bug.objects.filter(is_deleted='FALSE',
                  requirement=location_id)
            else:
                bug_results = bug.objects.filter(is_deleted='FALSE')
    if destination == None:
        t = loader.get_template('NearBeach/bug_list.html')
    else:
        t = loader.get_template('NearBeach/bug_list_specific.html')
    c = {'bug_results': bug_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def bug_search(request, location_id=None, destination=None):
    bug_results = None
    bug_client_id = None
    if request.method == 'POST':
        form = bug_search_form(request.POST)
        if form.is_valid():
            bug_client_instance = bug_client.objects.get(bug_client_id=(form.data['list_of_bug_client']))
            bug_client_id = bug_client_instance.bug_client_id
            if destination == 'project':
                existing_bugs = bug.objects.filter(is_deleted='FALSE',
                  project=location_id,
                  bug_client_id=bug_client_id)
            else:
                if destination == 'task':
                    existing_bugs = bug.objects.filter(is_deleted='FALSE',
                      task=location_id,
                      bug_client_id=bug_client_id)
                else:
                    existing_bugs = bug.objects.filter(is_deleted='FALSE',
                      requirement=location_id,
                      bug_client_id=bug_client_id)
            f_bugs = ''
            o_notequals = ''
            v_values = ''
            for idx, row in enumerate(existing_bugs):
                nidx = str(idx + 1)
                f_bugs = f_bugs + '&f' + nidx + '=bug_id'
                o_notequals = o_notequals + '&o' + nidx + '=notequals'
                v_values = v_values + '&v' + nidx + '=' + str(row.bug_code)

            exclude_url = f_bugs + o_notequals + v_values
            url = bug_client_instance.bug_client_url + bug_client_instance.list_of_bug_client.bug_client_api_url + bug_client_instance.list_of_bug_client.api_search_bugs + form.cleaned_data['search'] + exclude_url
            if url.lower().startswith('http'):
                req = urllib.request.Request(url)
            else:
                raise ValueError from None
            with urllib.request.urlopen(req) as (response):
                json_data = json.load(response)
            bug_results = json_data['bugs']
        else:
            print(form.errors)
    t = loader.get_template('NearBeach/bug_search.html')
    c = {'bug_search_form':bug_search_form(request.POST or None), 
     'bug_results':bug_results, 
     'location_id':location_id, 
     'destination':destination, 
     'bug_client_id':bug_client_id}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def campus_information(request, campus_information):
    permission_results = return_user_permission_level(request, None, 'organisation_campus')
    if permission_results['organisation_campus'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    campus_results = campus.objects.get(pk=campus_information)
    if campus_results.campus_longitude == None:
        update_coordinates(campus_information)
    if request.method == 'POST':
        print('\n\nREQUEST POST\n')
        print(request.POST)
        print('END REQUEST POST\n\n')
        form = campus_information_form(request.POST)
        if form.is_valid():
            campus_results.campus_nickname = form.cleaned_data['campus_nickname']
            campus_results.campus_phone = request.POST.get('hidden_campus_phone')
            campus_results.campus_fax = request.POST.get('hidden_campus_fax')
            campus_results.campus_address1 = form.cleaned_data['campus_address1']
            campus_results.campus_address2 = form.cleaned_data['campus_address2']
            campus_results.campus_address3 = form.cleaned_data['campus_address3']
            campus_results.campus_suburb = form.cleaned_data['campus_suburb']
            campus_results.change_user = request.user
            campus_results.save()
            update_coordinates(campus_information)
        if 'add_customer_submit' in request.POST:
            customer_results = int(request.POST.get('add_customer_select'))
            customer_instance = customer.objects.get(customer_id=customer_results)
            campus_instances = campus.objects.get(campus_id=campus_information)
            submit_campus = customer_campus(customer_id=customer_instance,
              campus_id=campus_instances,
              customer_phone='',
              customer_fax='',
              change_user=(request.user))
            submit_campus.save()
            return HttpResponseRedirect(reverse('customer_campus_information', args={submit_campus.customer_campus_id, 'CAMP'}))
    customer_campus_results = customer_campus.objects.filter(campus_id=campus_information,
      is_deleted='FALSE')
    add_customer_results = customer.objects.filter(organisation_id=(campus_results.organisation_id))
    countries_regions_results = list_of_country_region.objects.all()
    countries_results = list_of_country.objects.all()
    MAPBOX_API_TOKEN = ''
    GOOGLE_MAP_API_TOKEN = ''
    if hasattr(settings, 'MAPBOX_API_TOKEN'):
        MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN
        print('Got mapbox API token: ' + MAPBOX_API_TOKEN)
    else:
        if hasattr(settings, 'GOOGLE_MAP_API_TOKEN'):
            GOOGLE_MAP_API_TOKEN = settings.GOOGLE_MAP_API_TOKEN
            print('Got Google Maps API token: ' + GOOGLE_MAP_API_TOKEN)
        t = loader.get_template('NearBeach/campus_information.html')
        c = {'campus_results':campus_results, 
         'campus_information_form':campus_information_form(instance=campus_results), 
         'campus_permission':permission_results['organisation_campus'], 
         'customer_campus_results':customer_campus_results, 
         'add_customer_results':add_customer_results, 
         'countries_regions_results':countries_regions_results, 
         'countries_results':countries_results, 
         'permission':permission_results['organisation_campus'], 
         'new_item_permission':permission_results['new_item'], 
         'administration_permission':permission_results['administration'], 
         'MAPBOX_API_TOKEN':MAPBOX_API_TOKEN, 
         'GOOGLE_MAP_API_TOKEN':GOOGLE_MAP_API_TOKEN}
        return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def campus_readonly(request, campus_information):
    permission_results = return_user_permission_level(request, None, 'organisation_campus')
    if permission_results['organisation_campus'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    campus_results = campus.objects.get(pk=campus_information)
    if campus_results.campus_longitude == None:
        update_coordinates(campus_information)
    else:
        customer_campus_results = customer_campus.objects.filter(campus_id=campus_information,
          is_deleted='FALSE')
        add_customer_results = customer.objects.filter(organisation_id=(campus_results.organisation_id))
        countries_regions_results = list_of_country_region.objects.all()
        countries_results = list_of_country.objects.all()
        MAPBOX_API_TOKEN = ''
        GOOGLE_MAP_API_TOKEN = ''
        if hasattr(settings, 'MAPBOX_API_TOKEN'):
            MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN
            print('Got mapbox API token: ' + MAPBOX_API_TOKEN)
        else:
            if hasattr(settings, 'GOOGLE_MAP_API_TOKEN'):
                GOOGLE_MAP_API_TOKEN = settings.GOOGLE_MAP_API_TOKEN
                print('Got Google Maps API token: ' + GOOGLE_MAP_API_TOKEN)
    t = loader.get_template('NearBeach/campus_readonly.html')
    c = {'campus_results':campus_results, 
     'campus_readonly_form':campus_readonly_form(instance=campus_results), 
     'customer_campus_results':customer_campus_results, 
     'add_customer_results':add_customer_results, 
     'countries_regions_results':countries_regions_results, 
     'countries_results':countries_results, 
     'permission':permission_results['organisation_campus'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'MAPBOX_API_TOKEN':MAPBOX_API_TOKEN, 
     'GOOGLE_MAP_API_TOKEN':GOOGLE_MAP_API_TOKEN}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def change_group_leader(request, user_group_id):
    """
    This is an administration task. On the groups information page, an administrator might want to make sure that a user
    is a group leader (or remove them), they will click on the hyperlink to do so. This function is then called.

    It will change the group leader status to the opposite boolean
    TRUE -> FALSE
    FALSE -> TRUE
    :param request:
    :param user_group_id: The user_group_id we are focusing on flipping
    :return: blank page

    Method
    ~~~~~~
    1. Make sure this method is done in POST
    2. Make sure the user has correct permissions
    3. Find ALL user_group permissions with the group/user filters
    4. Apply the BOOLEAN SWITCH
    5. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, ['administration'])
        if permission_results['administration'] <= 1:
            return HttpResponseRedirect(reverse('permission_denied'))
        else:
            user_group_results = user_group.objects.get(user_group_id=user_group_id)
            if user_group_results.group_leader == 'TRUE':
                user_group_results.group_leader = 'FALSE'
            else:
                user_group_results.group_leader = 'TRUE'
        user_group_results.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Can only be done through Post')


@login_required(login_url='login', redirect_field_name='')
def change_task_edit(request, change_task_id):
    """
    This will display the user's change request. If it is read only then it will utilise the read only template
    :param request:
    :param change_task_id: The change task we are going to use
    :return: Rendered page

    Method
    ~~~~~~
    1. Check user permissions
    2. Check to see if method is POST - take not of change there
    3. Gather data from database
    4. Get template
    5. Render
    """
    change_task_results = change_task.objects.get(change_task_id=change_task_id)
    rfc_results = request_for_change.objects.get(rfc_id=(change_task_results.request_for_change_id))
    group_results = object_assignment.objects.filter(is_deleted='FALSE',
      request_for_change_id=(change_task_results.request_for_change_id)).values('group_id')
    permission_results = return_user_permission_level(request, group_results, ['request_for_change'])
    if permission_results['request_for_change'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    else:
        return permission_results['request_for_change'] == 1 or rfc_results.rfc_status == 1 or HttpResponseRedirect(reverse('change_task_information', args={change_task_id}))
    if request.method == 'POST':
        form = change_task_form((request.POST),
          rfc_id=(change_task_results.request_for_change_id))
        print('GOT HERE!')
        if form.is_valid():
            change_task_results.change_task_title = form.cleaned_data['change_task_title']
            change_task_results.change_task_start_date = form.cleaned_data['change_task_start_date']
            change_task_results.change_task_end_date = form.cleaned_data['change_task_end_date']
            change_task_results.change_task_assigned_user = form.cleaned_data['change_task_assigned_user']
            change_task_results.change_task_qa_user = form.cleaned_data['change_task_qa_user']
            change_task_results.change_task_description = form.cleaned_data['change_task_description']
            change_task_results.change_task_required_by = form.cleaned_data['change_task_required_by']
            change_task_results.change_user = request.user
            start_date = form.cleaned_data['change_task_start_date']
            end_date = form.cleaned_data['change_task_end_date']
            change_task_results.change_task_seconds = (end_date - start_date).total_seconds()
            change_task_results.save()
            return HttpResponseRedirect(reverse('request_for_change_draft',
              args={
             change_task_results.request_for_change_id}))
        print(form.errors)
    t = loader.get_template('NearBeach/request_for_change/change_task_edit.html')
    c = {'change_task_results':change_task_results, 
     'change_task_form':change_task_form(rfc_id=change_task_results.request_for_change_id,
       initial={'change_task_title':change_task_results.change_task_title, 
      'change_task_start_date':change_task_results.change_task_start_date, 
      'change_task_end_date':change_task_results.change_task_end_date, 
      'change_task_assigned_user':change_task_results.change_task_assigned_user, 
      'change_task_qa_user':change_task_results.change_task_qa_user, 
      'change_task_description':change_task_results.change_task_description, 
      'change_task_required_by':change_task_results.change_task_required_by}), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def change_task_finish(request, change_task_id):
    """
    This will finish the change task.
    :param request:
    :param change_task_id:
    :return:
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'request_for_change')
        if permission_results['request_for_change'] <= 1:
            return HttpResponseRedirect(reverse('permission_denied'))
        change_task.objects.filter(change_task_id=change_task_id).update(change_task_status=5)
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - this can only be done through post')


@login_required(login_url='login', redirect_field_name='')
def change_task_information(request, change_task_id):
    """
    This will display the user's change request in READ ONLY format.
    :param request:
    :param change_task_id: The change task we are going to use
    :return: Rendered page

    Method
    ~~~~~~
    1. Check user permissions
    2. Gather data from database
    3. Get template
    4. Render
    """
    change_task_results = change_task.objects.get(change_task_id=change_task_id)
    group_results = object_assignment.objects.filter(is_deleted='FALSE',
      request_for_change_id=(change_task_results.request_for_change_id)).values('group_id')
    permission_results = return_user_permission_level(request, group_results, ['request_for_change'])
    if permission_results['request_for_change'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    t = loader.get_template('NearBeach/request_for_change/change_task_information.html')
    c = {'change_task_results':change_task_results, 
     'change_task_form':change_task_read_only_form(initial={'change_task_description': change_task_results.change_task_description}), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def change_task_list(request, rfc_id):
    """
    When a user is looking at a request for change, they will need to see ALL change tasks associated with this rfc.
    This will call this function through AJAX. This function will then deliver a simple and effecting RUN LIST/CHANGE TASKS
    :param request:
    :param rfc_id: The request for change we are looking at.
    :return: The RUN LIST/CHANGE TASKS

    Method
    ~~~~~~
    1. Check user permissions
    2. Obtain the SQL required
    3. Get template and context
    4. Render and send to the user.
    """
    permission_results = return_user_permission_level(request, None, 'request_for_change')
    if permission_results['request_for_change'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    else:
        change_task_results = change_task.objects.filter(is_deleted='FALSE',
          request_for_change=rfc_id).order_by('change_task_start_date', 'change_task_end_date', 'change_task_assigned_user', 'change_task_qa_user')
        change_task_seconds = change_task_results.aggregate(Sum('change_task_seconds'))
        if not change_task_seconds['change_task_seconds__sum'] == None:
            change_task_seconds = datetime.datetime.fromtimestamp(change_task_seconds['change_task_seconds__sum']).strftime('Days - %d, Hours - %H, Minutes - %m')
        else:
            change_task_seconds = 'Please enter a change task'
    assigned_user_results = User.objects.filter(is_active=True,
      id__in=(change_task_results.values('change_task_assigned_user')))
    qa_user_results = User.objects.filter(is_active=True,
      id__in=(change_task_results.values('change_task_qa_user')))
    rfc_status = request_for_change.objects.get(rfc_id=rfc_id).rfc_status
    t = loader.get_template('NearBeach/request_for_change/change_task_list.html')
    c = {'change_task_results':change_task_results, 
     'permission':permission_results['request_for_change'], 
     'rfc_id':rfc_id, 
     'rfc_status':rfc_status, 
     'assigned_user_results':assigned_user_results, 
     'qa_user_results':qa_user_results, 
     'change_task_seconds':change_task_seconds}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def change_task_start(request, change_task_id):
    """
    This will start the change task.
    :param request:
    :param change_task_id:
    :return:
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'request_for_change')
        if permission_results['request_for_change'] <= 1:
            return HttpResponseRedirect(reverse('permission_denied'))
        change_task.objects.filter(change_task_id=change_task_id).update(change_task_status=4)
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - this can only be done through post')


@login_required(login_url='login', redirect_field_name='')
def cost_information(request, location_id, destination):
    if destination == 'project':
        groups_results = object_assignment.objects.filter(is_deleted='FALSE',
          project_id=project.objects.get(project_id=location_id)).values('group_id_id')
    else:
        groups_results = object_assignment.objects.filter(is_deleted='FALSE',
          task_id=task.objects.get(task_id=location_id)).values('group_id_id')
    permission_results = return_user_permission_level(request, groups_results, destination)
    if request.method == 'POST':
        form = cost_information_form(request.POST, request.FILES)
        if form.is_valid():
            cost_description = form.cleaned_data['cost_description']
            cost_amount = form.cleaned_data['cost_amount']
            if not cost_description == '':
                if cost_amount <= 0 or cost_amount >= 0:
                    submit_cost = cost(cost_description=cost_description,
                      cost_amount=cost_amount,
                      change_user=(request.user))
                    if destination == 'project':
                        submit_cost.project_id = project.objects.get(project_id=location_id)
                    else:
                        if destination == 'task':
                            submit_cost.task_id = task.objects.get(task_id=location_id)
                    submit_cost.save()
    elif destination == 'project':
        costs_results = cost.objects.filter(project_id=location_id, is_deleted='FALSE')
    else:
        costs_results = cost.objects.filter(task_id=location_id, is_deleted='FALSE')
    running_total = []
    grand_total = 0
    for line_item in costs_results:
        grand_total = grand_total + float(line_item.cost_amount)
        running_total.append(grand_total)

    cost_zip_results = zip(costs_results, running_total)
    t = loader.get_template('NearBeach/costs.html')
    c = {'cost_information_form':cost_information_form(), 
     'cost_zip_results':cost_zip_results, 
     'cost_permissions':permission_results[destination], 
     'grand_total':grand_total}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def customer_campus_information(request, customer_campus_id, customer_or_org):
    permission_results = return_user_permission_level(request, None, 'organisation_campus')
    if permission_results['organisation_campus'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        if permission_results['organisation_campus'] > 1:
            form = customer_campus_form(request.POST)
            if form.is_valid():
                save_data = customer_campus.objects.get(customer_campus_id=customer_campus_id)
                save_data.customer_phone = form.cleaned_data['customer_phone']
                save_data.customer_fax = form.cleaned_data['customer_fax']
                save_data.change_user = request.user
                save_data.save()
                if customer_or_org == 'CAMP':
                    return HttpResponseRedirect(reverse('campus_information', args={save_data.campus_id.campus_id}))
                return HttpResponseRedirect(reverse('customer_information', args={save_data.customer_id.customer_id}))
    else:
        customer_campus_results = customer_campus.objects.get(customer_campus_id=customer_campus_id)
        campus_results = campus.objects.get(pk=(customer_campus_results.campus_id.campus_id))
        initial = {'customer_phone':customer_campus_results.customer_phone, 
         'customer_fax':customer_campus_results.customer_fax}
        if hasattr(settings, 'MAPBOX_API_TOKEN'):
            MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN
            print('Got mapbox API token: ' + MAPBOX_API_TOKEN)
        else:
            MAPBOX_API_TOKEN = ''
    MAPBOX_API_TOKEN = ''
    GOOGLE_MAP_API_TOKEN = ''
    if hasattr(settings, 'MAPBOX_API_TOKEN'):
        MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN
        print('Got mapbox API token: ' + MAPBOX_API_TOKEN)
    else:
        if hasattr(settings, 'GOOGLE_MAP_API_TOKEN'):
            GOOGLE_MAP_API_TOKEN = settings.GOOGLE_MAP_API_TOKEN
            print('Got Google Maps API token: ' + GOOGLE_MAP_API_TOKEN)
        t = loader.get_template('NearBeach/customer_campus.html')
        c = {'customer_campus_form':customer_campus_form(initial=initial), 
         'customer_campus_results':customer_campus_results, 
         'customer_campus_id':customer_campus_id, 
         'customer_or_org':customer_or_org, 
         'permission':permission_results['organisation_campus'], 
         'new_item_permission':permission_results['new_item'], 
         'administration_permission':permission_results['administration'], 
         'campus_results':campus_results, 
         'MAPBOX_API_TOKEN':MAPBOX_API_TOKEN, 
         'GOOGLE_MAP_API_TOKEN':GOOGLE_MAP_API_TOKEN}
        return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def customer_information(request, customer_id):
    permission_results = return_user_permission_level(request, None, ['assign_campus_to_customer', 'customer'])
    if permission_results['customer'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
        if permission_results['customer'] == 1:
            return HttpResponseRedirect(reverse('customer_readonly', args={customer_id}))
        if request.method == 'POST' and permission_results['customer'] > 1:
            form = customer_information_form(request.POST, request.FILES)
            if form.is_valid():
                current_user = request.user
                save_data = customer.objects.get(customer_id=customer_id)
                save_data.customer_title = form.cleaned_data['customer_title']
                save_data.customer_first_name = form.cleaned_data['customer_first_name']
                save_data.customer_last_name = form.cleaned_data['customer_last_name']
                save_data.customer_email = form.cleaned_data['customer_email']
                save_data.change_user = request.user
                update_profile_picture = request.FILES.get('update_profile_picture')
                if not update_profile_picture == None:
                    save_data.customer_profile_picture = update_profile_picture
                save_data.save()
    else:
        print(form.errors)
    customer_results = get_object_or_404(customer,
      customer_id=customer_id,
      is_deleted='FALSE')
    add_campus_results = campus.objects.filter(organisation_id=(customer_results.organisation_id),
      is_deleted='FALSE')
    quote_results = quote.objects.filter(is_deleted='FALSE',
      customer_id=customer_id)
    project_results = project.objects.filter(is_deleted='FALSE',
      project_id__in=(project_customer.objects.filter(is_deleted='FALSE',
      customer_id=customer_id).values('project_id')))
    task_results = task.objects.filter(is_deleted='FALSE',
      task_id__in=(task_customer.objects.filter(is_deleted='FALSE',
      customer_id=customer_id).values('task_id')))
    user_groups_results = user_group.objects.filter(username=(request.user))
    opportunity_permissions_results = object_assignment.objects.filter(Q(Q(assigned_user=(request.user)) | Q(group_id__in=(user_groups_results.values('group_id')))))
    opportunity_results = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      customer_id=customer_id,
      opportunity_id__in=(opportunity_permissions_results.values('opportunity_id'))).values('opportunity_id')))
    campus_results = customer_campus.objects.filter(customer_id=customer_id,
      is_deleted='FALSE')
    customer_campus_results = campus.objects.filter(is_deleted='FALSE',
      customer=customer_id)
    try:
        profile_picture = customer_results.customer_profile_picture.url
    except:
        profile_picture = ''

    t = loader.get_template('NearBeach/customer_information.html')
    c = {'customer_information_form':customer_information_form(instance=customer_results), 
     'campus_results':campus_results, 
     'customer_campus_results':customer_campus_results, 
     'add_campus_results':add_campus_results, 
     'customer_results':customer_results, 
     'media_url':settings.MEDIA_URL, 
     'profile_picture':profile_picture, 
     'project_results':project_results, 
     'task_results':task_results, 
     'opportunity_results':opportunity_results, 
     'PRIVATE_MEDIA_URL':settings.PRIVATE_MEDIA_URL, 
     'customer_id':customer_id, 
     'customer_permissions':permission_results['customer'], 
     'assign_campus_to_customer_permission':permission_results['assign_campus_to_customer'], 
     'quote_results':quote_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def customer_readonly(request, customer_id):
    permission_results = return_user_permission_level(request, None, ['assign_campus_to_customer', 'customer'])
    if permission_results['customer'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    customer_results = customer.objects.get(customer_id=customer_id,
      is_deleted='FALSE')
    add_campus_results = campus.objects.filter(organisation_id=(customer_results.organisation_id),
      is_deleted='FALSE')
    quote_results = quote.objects.filter(is_deleted='FALSE',
      customer_id=customer_id)
    project_results = project.objects.filter(is_deleted='FALSE',
      project_id__in=(project_customer.objects.filter(is_deleted='FALSE',
      customer_id=customer_id).values('project_id')))
    task_results = task.objects.filter(is_deleted='FALSE',
      task_id__in=(task_customer.objects.filter(is_deleted='FALSE',
      customer_id=customer_id).values('task_id')))
    contact_history_results = contact_history.objects.filter(is_deleted='FALSE',
      customer_id=customer_id)
    contact_history_collective = []
    for row in contact_history_results:
        contact_history_collective.append(contact_history_readonly_form(initial={'contact_history':row.contact_history, 
         'submit_history':row.user_id.username + ' - ' + row.date_created.strftime('%d %B %Y %H:%M.%S')},
          contact_history_id=(row.contact_history_id)))

    email_results = email_content.objects.filter(is_deleted='FALSE',
      email_content_id__in=(email_contact.objects.filter((Q(to_customer=customer_id) | Q(cc_customer=customer_id)) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
    user_groups_results = user_group.objects.filter(username=(request.user))
    opportunity_permissions_results = object_assignment.objects.filter(Q(Q(assigned_user=(request.user)) | Q(group_id__in=(user_groups_results.values('group_id')))))
    opportunity_results = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_id__in=(object_assignment.objects.filter(customer_id=customer_id,
      opportunity_id__in=(opportunity_permissions_results.values('opportunity_id'))).values('opportunity_id')))
    campus_results = customer_campus.objects.filter(customer_id=customer_id,
      is_deleted='FALSE')
    customer_campus_results = campus.objects.filter(is_deleted='FALSE',
      customer=customer_id)
    try:
        profile_picture = customer_results.customer_profile_picture.url
    except:
        profile_picture = ''

    t = loader.get_template('NearBeach/customer_information/customer_readonly.html')
    c = {'customer_readonly_form':customer_readonly_form(instance=customer_results), 
     'campus_results':campus_results, 
     'customer_campus_results':customer_campus_results, 
     'add_campus_results':add_campus_results, 
     'customer_results':customer_results, 
     'media_url':settings.MEDIA_URL, 
     'profile_picture':profile_picture, 
     'project_results':project_results, 
     'task_results':task_results, 
     'opportunity_results':opportunity_results, 
     'PRIVATE_MEDIA_URL':settings.PRIVATE_MEDIA_URL, 
     'customer_id':customer_id, 
     'customer_permissions':permission_results['customer'], 
     'assign_campus_to_customer_permission':permission_results['assign_campus_to_customer'], 
     'quote_results':quote_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'contact_history_collective':contact_history_collective, 
     'email_results':email_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard(request):
    """
    Due to a bug - if the user goes to /admin/ and logs in there, they will by pass this one session request. It is
    placed here to make sure. :)
    """
    request.session['is_superuser'] = request.user.is_superuser
    permission_results = return_user_permission_level(request, None, 'project')
    t = loader.get_template('NearBeach/dashboard.html')
    c = {'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_active_bugs(request):
    """
    This will render a simple widget that will display the state of each bug client.
    :param request:
    :return:

    Method
    ~~~~~~
    1. Get a list of all bug clients still active
    2. Declare variables
    3. Loop through list of bug clients
    -- START LOOP --
        4. Get the url for the API
        5. Fetch the JSON data
        6. Create basic pivot table
        7. Return results
    -- END LOOP --
    8. Send the JSON results to the template

                if url.lower().startswith('http'):
                    req = urllib.request.Request(url)
                else:
                    raise ValueError from None

                with urllib.request.urlopen(req) as response: #nosec
                    data = json.load(response)

                bug_client_submit = bug_client(
                    bug_client_name = bug_client_name,
                    list_of_bug_client = list_of_bug_client,
                    bug_client_url = bug_client_url,
                    change_user=request.user,
                )
                bug_client_submit.save()
                return HttpResponseRedirect(reverse('bug_client_list'))

    """
    bug_client_results = bug_client.objects.filter(is_deleted='FALSE')
    bug_client_table = {}
    for counter, client in enumerate(bug_client_results):
        url = client.bug_client_url + '/rest/bug?resolution=---'
        status_results = {}
        if url.lower().startswith('http'):
            raw_data = requests.get(url).json()
        else:
            continue
        for bug_info in raw_data['bugs']:
            try:
                status_results[bug_info['status']] = status_results[bug_info['status']] + 1
            except:
                status_results[bug_info['status']] = 1

        status_results = {'bug_client_id':client.bug_client_id, 
         'name':client.bug_client_name, 
         'url':client.bug_client_url, 
         'bug_status':status_results}
        bug_client_table[counter] = status_results

    return JsonResponse(bug_client_table, safe=False)


@login_required(login_url='login', redirect_field_name='')
def dashboard_active_projects(request):
    assigned_users_results = object_assignment.objects.filter(is_deleted='FALSE',
      assigned_user=(request.user),
      project_id__isnull=False).exclude(project_id__project_status='Closed').values('project_id__project_id', 'project_id__project_name', 'project_id__project_end_date', 'project_id__project_start_date').distinct()
    object_assignment_results = object_assignment.objects.filter(is_deleted='FALSE',
      project_id__in=(assigned_users_results.values('project_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/active_projects.html')
    c = {'assigned_users_results':assigned_users_results, 
     'object_assignment_results':object_assignment_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_active_quotes(request):
    quote_results = quote.objects.filter(is_deleted='FALSE',
      quote_stage_id__in=(list_of_quote_stage.objects.filter(quote_closed='FALSE').values('quote_stage_id')),
      quote_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id'))).values('quote_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/active_quotes.html')
    c = {'quote_results': quote_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_active_requirement(request):
    requirement_results = requirement.objects.filter(is_deleted='FALSE',
      requirement_status__in=(list_of_requirement_status.objects.filter(requirement_status_is_closed='FALSE').values('requirement_status_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/active_requirements.html')
    c = {'requirement_results': requirement_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_active_task(request):
    assigned_users_results = object_assignment.objects.filter(is_deleted='FALSE',
      assigned_user=(request.user),
      task_id__isnull=False).exclude(task_id__task_status='Closed').values('task_id__task_id', 'task_id__task_short_description', 'task_id__task_end_date', 'task_id__task_start_date').distinct()
    object_assignment_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id__in=(assigned_users_results.values('task_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/active_tasks.html')
    c = {'assigned_users_results':assigned_users_results, 
     'object_assignment_results':object_assignment_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_administration_task(request):
    """
    This dashbaord widget just shows a simple list of objects to complete for any NEW instances.

    Essentially - we will look at each object and see if there has been anything created (i.e. has a count greater than
    the initial setup number).
    :param request:
    :return:
    """
    group_results = group.objects.filter(Q(is_deleted='FALSE') & ~Q(group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      group_leader='TRUE').values('group'))))
    t = loader.get_template('NearBeach/dashboard_widgets/administration_task.html')
    c = {'permission_setup':permission_set.objects.filter(is_deleted='FALSE').count() > 1, 
     'group_setup':group.objects.filter(is_deleted='FALSE').count() > 1, 
     'user_setup':User.objects.filter(is_active=True).count() > 1, 
     'product_setup':product_and_service.objects.filter(is_deleted='FALSE').count() > 0, 
     'tax_setup':list_of_tax.objects.filter(is_deleted='FALSE').count() > 0, 
     'quote_template_setup':quote_template.objects.filter(is_deleted='FALSE').count() > 0, 
     'group_results':group_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_group_active_projects(request):
    active_projects_results = project.objects.filter(is_deleted='FALSE',
      project_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username_id=(request.user.id)).values('group'))).values('project_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/group_active_projects.html')
    c = {'active_projects_results': active_projects_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_group_active_task(request):
    active_task_results = task.objects.filter(is_deleted='FALSE',
      task_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username_id=(request.user)).values('group_id'))).values('task_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/group_active_tasks.html')
    c = {'active_task_results': active_task_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_group_opportunities(request):
    active_group_opportunities = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username_id=(request.user)).values('group_id'))).values('opportunity_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/group_opportunities.html')
    c = {'active_group_opportunities': active_group_opportunities}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_group_request_for_change(request):
    """
    A simple dashboard widget that shows currently all RFC's that the user has access to through their group.
    :param request:
    :return:
    """
    rfc_results = request_for_change.objects.filter(is_deleted='FALSE',
      rfc_status__in=[
     1, 2, 3, 4],
      rfc_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      request_for_change__isnull=False,
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id'))).values('request_for_change')))
    t = loader.get_template('NearBeach/dashboard_widgets/group_request_for_change.html')
    c = {'rfc_results': rfc_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_opportunities(request):
    active_opportunities = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_stage_id__in=list_of_opportunity_stage.objects.filter(opportunity_closed='FALSE'),
      opportunity_id__in=(object_assignment.objects.filter(Q(is_deleted='FALSE') and Q(Q(assigned_user=(request.user)) or Q(group_id__in=user_group.objects.filter(username=(request.user),
      is_deleted='FALSE')))).values('opportunity_id')))
    t = loader.get_template('NearBeach/dashboard_widgets/opportunities.html')
    c = {'active_opportunities': active_opportunities}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def dashboard_ready_for_approval(request):
    """
    This dashboard widget will show the user if there are any objects that require their attention for approval.
    This dashboard widget is currently just focused on Request for Change, however can be utilised for any objects
    in the future
    :param request:
    :return: Widget

    Method
    ~~~~~~
    1. Obtain SQL
    2. Get template and context
    3. Render
    """
    user_group_results = user_group.objects.filter(is_deleted='FALSE',
      group_leader='TRUE',
      username=(request.user))
    rfc_results = request_for_change.objects.filter(is_deleted='FALSE',
      rfc_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      request_for_change__isnull=False,
      group_id__in=(user_group_results.values('group_id'))).values('request_for_change')),
      rfc_status=2)
    t = loader.get_template('NearBeach/dashboard_widgets/ready_for_approval.html')
    c = {'rfc_results': rfc_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def deactivate_campus(request, campus_id):
    if request.method == 'POST':
        campus_update = campus.objects.get(campus_id=campus_id)
        campus_update.is_deleted = 'TRUE'
        campus_update.save()
        customer_campus.objects.filter(is_deleted='FALSE',
          campus_id=campus_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this request is only for POST')


@login_required(login_url='login', redirect_field_name='')
def delete_campus_contact(request, customer_campus_id, cust_or_camp):
    """
    So... I will need to add in security to define IF a user can do this action
    """
    save_customer_campus = customer_campus.objects.get(pk=customer_campus_id)
    save_customer_campus.is_deleted = 'TRUE'
    save_customer_campus.change_user = request.user
    save_customer_campus.save()
    if cust_or_camp == 'CAMP':
        return HttpResponseRedirect(reverse('campus_information', args={save_customer_campus.campus_id.organisations_campus_id}))
    return HttpResponseRedirect(reverse('customer_information', args={save_customer_campus.customer_id.customer_id}))


@login_required(login_url='login', redirect_field_name='')
def delete_cost(request, cost_id, location_id, project_or_task):
    cost_save = cost.objects.get(pk=cost_id)
    cost_save.is_deleted = 'TRUE'
    cost_save.change_user = request.user
    cost_save.save()
    if project_or_task == 'P':
        return HttpResponseRedirect(reverse('project_information', args={location_id}))
    return HttpResponseRedirect(reverse('task_information', args={location_id}))


@login_required(login_url='login', redirect_field_name='')
def delete_customer(request, customer_id):
    """
    This will remove the customer and ANY connections it has with any object. This can not be undone.
    :param request:
    :param organisation_id: the organisation we will delete
    :return: Blank page

    Method
    ~~~~~~
    1. Check to make sure it is in POST - send error otherwise
    2. Check to make sure user has permission - if not send them to the naughty place
    3. Delete the organisation
    4. Delete the customers connected to the organisation
    5. Delete any object connected to the organisation
    6. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'customer')
        if permission_results['customer'] < 4:
            return HttpResponseRedirect(reverse('permission_denied'))
        customer.objects.filter(customer_id=customer_id).update(is_deleted='TRUE')
        print('DELETED CUSTOMER')
        project_customer.objects.filter(is_deleted='FALSE',
          customer_id=customer_id).update(is_deleted='TRUE')
        task_customer.objects.filter(is_deleted='FALSE',
          customer_id=customer_id).update(is_deleted='TRUE')
        object_assignment.objects.filter(is_deleted='FALSE',
          customer_id=customer_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Can only do this in POST')


@login_required(login_url='login', redirect_field_name='')
def delete_group(request, group_id):
    """
    This will remove the group, and anyone connected to the group. Becareful - this is a sad function.
    :param request:
    :param group_id: The group we wish to delete
    :return: blank page

    Method
    ~~~~~~
    1. Check to see if the request is in POST - if not send user an error
    2. Check to see if the user has permission - if not, send them to the naughty corner
    3. Get the group using the group_id - set is_deleted to TRUE
    4. Filter user_group by the group_id
    5. Set the filtered user_group data field is_deleted to TRUE
    6. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'administration_create_group')
        if permission_results['administration_create_group'] < 4:
            return HttpResponseBadRequest('You do not have permission to delete')
        if group_id == 1 or group_id == '1':
            group_id = 0
        group.objects.filter(group_id=group_id).update(is_deleted='TRUE')
        user_group.objects.filter(is_deleted='FALSE',
          group_id=group_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - can only be done in POST')


@login_required(login_url='login', redirect_field_name='')
def delete_organisation(request, organisation_id):
    """
    This will remove the organisation and ANY connections it has with any object. This can not be undone.
    :param request:
    :param organisation_id: the organisation we will delete
    :return: Blank page

    Method
    ~~~~~~
    1. Check to make sure it is in POST - send error otherwise
    2. Check to make sure user has permission - if not send them to the naughty place
    3. Delete the organisation
    4. Delete the customers connected to the organisation
    5. Delete any object connected to the organisation
    6. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'organisation')
        if permission_results['organisation'] < 4:
            return HttpResponseRedirect(reverse('permission_denied'))
        organisation_update = organisation.objects.filter(organisation_id=organisation_id).update(is_deleted='TRUE')
        customer_update = customer.objects.filter(is_deleted='FALSE',
          organisation_id=organisation_id).update(is_deleted='TRUE')
        project_update = project.objects.filter(is_deleted='FALSE',
          organisation_id=organisation_id).update(is_deleted='TRUE')
        task_update = task.objects.filter(is_deleted='FALSE',
          organisation_id=organisation_id).update(is_deleted='TRUE')
        object_assignment_update = object_assignment.objects.filter(is_deleted='FALSE',
          organisation_id=organisation_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Can only do this in POST')


@login_required(login_url='login', redirect_field_name='')
def delete_permission_set(request, permission_set_id):
    """
    This will remove a permission set along with any user_group's connected to this permission_set. Becareful
    :param request:
    :param permission_set_id: the permission set we are removing
    :return: blank page

    Method
    ~~~~~~
    1. Check to make sure it is in POST - otherwise throw error
    2. Check to make sure user has permission - otherwise throw error
    3. Get the permission_set using permission_set id - update is_deleted to TRUE
    4. Find all user_group rows connected with this permission_set - update is_deleted to True
    5. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'administration_create_permission_set')
        if permission_results['administration_create_permission_set'] < 4:
            return HttpResponseBadRequest('You do not have permission to delete')
        permission_set.objects.filter(permission_set_id=permission_set_id).update(is_deleted='TRUE')
        user_group.objects.filter(is_deleted='FALSE',
          permission_set_id=permission_set_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - can only do this in POST')


@login_required(login_url='login', redirect_field_name='')
def delete_tag(request, tag_id):
    """
    Delete tag will actually remove the tag and all it's assignments from the system.

    Only a user with a tag permission of 4 can do this task.

    :param request:
    :param tag_id: the tag to delete
    :return: blank page if successful

    Method
    ~~~~~~
    1. Check permissions - if use does not pass send them to the naughty corner
    2. Check to make sure is in POST - if not, return an error
    3. Delete the tag
    4. Delete the tag assignments
    5. Return a blank page
    """
    permission_results = return_user_permission_level(request, None, 'tag')
    if permission_results['tag'] < 4:
        return HttpResponseForbidden
    if request.method == 'POST':
        update_tag = tag.objects.get(tag_id=tag_id)
        update_tag.is_deleted = 'TRUE'
        update_tag.save()
        update_tag_assignment = tag_assignment.objects.filter(is_deleted='FALSE',
          tag_id=tag_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this can only be done through POST')


@login_required(login_url='login', redirect_field_name='')
def delete_tag_from_object(request, tag_id, location_id, destination):
    """
    If the user has permission, we will delete the tag from the current object location.

    Please note - a user might accidently type in the same tag multiple times. Hence we are just getting tag
    id, location_id and destination and removing ALL tags with the same id from this object location
    :param request:
    :param tag_id: the tag_id that we are removing
    :param location_id: location id for the object
    :param destination: the destination of the object
    :return:

    Method
    ~~~~~~
    1. Make sure is post
    2. Make sure user has permission to delete
    3. Filter for all tags in current destination and location
    4. Delete :)
    5. Send back blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'tag')
        if permission_results['tag'] < 4:
            return HttpResponseBadRequest('You do not have permission to delete')
        elif destination == 'project':
            tag_assignment_update = tag_assignment.objects.filter(is_deleted='FALSE',
              tag_id=tag_id,
              project_id=location_id).update(is_deleted='TRUE')
        else:
            if destination == 'task':
                tag_assignment_update = tag_assignment.objects.filter(is_deleted='FALSE',
                  tag_id=tag_id,
                  task_id=location_id).update(is_deleted='TRUE')
            else:
                if destination == 'opportunity':
                    tag_assignment_update = tag_assignment.objects.filter(is_deleted='FALSE',
                      tag_id=tag_id,
                      opportunity_id=location_id).update(is_deleted='TRUE')
                else:
                    if destination == 'requirement':
                        tag_assignment_update = tag_assignment.objects.filter(is_deleted='FALSE',
                          tag_id=tag_id,
                          requirement_id=location_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this has to be done in POST')


@login_required(login_url='login', redirect_field_name='')
def delete_user_permission(request, user_id, permission_set_id, group_id):
    """
    This function will remove all permission sets for a particular group and user.

    Users can be added to the same collections of { group, permission_set } multiple times. We will need to delete all of
    these.
    :param request:
    :param user_id: Which user we are focusing on
    :param permission_set_id: Which permission set
    :param group_id:  Which group
    :return:

    Method
    ~~~~~~
    1. Check to make sure command is in POST - if not error out
    2. Check to make sure user has permission to do this - if not error out
    3. Filter the user_group for the; user_id, permission_set_id, and group_id
    4. Apply "is_deleted='TRUE'" to the filtered object
    5. Return blank page :)
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, [None], ['administration_create_group'])
        if not permission_results['administration_create_group'] == 4:
            return HttpResponseForbidden
        user_group_update = user_group.objects.filter(is_deleted='FALSE',
          group_id=group_id,
          permission_set_id=permission_set_id,
          username_id=user_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - can only do this in POST')


@login_required(login_url='login', redirect_field_name='')
def diagnostic_information(request):
    permission_results = return_user_permission_level(request, None, '')
    RECAPTCHA_PUBLIC_KEY = ''
    if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY'):
        RECAPTCHA_PUBLIC_KEY = settings.RECAPTCHA_PUBLIC_KEY
    t = loader.get_template('NearBeach/diagnostic_information.html')
    c = {'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'RECAPTCHA_PUBLIC_KEY':RECAPTCHA_PUBLIC_KEY, 
     'diagnostic_test_document_upload_form':diagnostic_test_document_upload_form()}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def diagnostic_render_pdf(request):
    """

    :param request:
    :return:

    """
    if request.get_host() == 'localhost:8000':
        url_path = 'http://' + request.get_host() + '/diagnostic_render_pdf/pdf_example/'
    else:
        url_path = 'https://' + request.get_host() + '/diagnostic_render_pdf/pdf_example/'
    html = HTML(url_path)
    pdf_results = html.write_pdf()
    response = HttpResponse(pdf_results, content_type='application')
    response['Content-Disposition'] = 'attachment; filename="Example PDF"'
    return response


@login_required(login_url='login', redirect_field_name='')
def diagnostic_test_database(request):
    """
    Ping the user's database. If there is an issue then report it
    """
    User.objects.filter(username=(request.user))
    t = loader.get_template('NearBeach/blank.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def diagnostic_test_document_upload(request):
    """
    Upload user's document and send back a link to the document. Please note the document will be fetched using
    ajax so test for any issues
    """
    print('Sending in test')
    if request.method == 'POST':
        print('Request is in post')
        if request.FILES == None:
            print('There was an error with the file')
            return HttpResponseBadRequest('File needs to be uploaded. Refresh the page and try again')
        print('Checking the file')
        file = request.FILES['document']
        print('Getting the filename string')
        filename = str(file)
        print('Saving the document')
        document_save = document(document_description=filename,
          document=file,
          change_user=(request.user))
        document_save.save()
        print('Saving document permissions')
        document_permissions_save = document_permission(document_key=document_save,
          change_user=(request.user))
        document_permissions_save.save()
        t = loader.get_template('NearBeach/diagnostic/test_document_download.html')
        c = {'document_key': document_save.document_key}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Something went wrong')


@login_required(login_url='login', redirect_field_name='')
def diagnostic_test_email(request):
    """
    Method
    ~~~~~~
    1.) Gather the required variables
    2.) Send an email to noreply@nearbeach.org
    3.) If the email fails at ANY point, send back an error
    4.) If the email works, send back a blank page
    """
    try:
        EMAIL_HOST_USER = settings.EMAIL_HOST_USER
        EMAIL_BACKEND = settings.EMAIL_BACKEND
        EMAIL_USE_TLS = settings.EMAIL_USE_TLS
        EMAIL_HOST = settings.EMAIL_HOST
        EMAIL_PORT = settings.EMAIL_PORT
        EMAIL_HOST_USER = settings.EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
    except:
        return HttpResponseBadRequest('Variables have not been fully setup in settings.py')
        try:
            email = EmailMultiAlternatives('NearBeach Diagnostic Test', 'Ignore email - diagnostic test', settings.EMAIL_HOST_USER, [
             'donotreply@nearbeach.org'])
            if not email.send():
                return HttpResponseBadRequest('Email did not send correctly.')
        except:
            return HttpResponseBadRequest('Email failed')

        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def diagnostic_test_location_services(request):
    """
    Method
    ~~~~~~
    1.) Check to make sure MAPBOX keys are inplace
    2.) If exists, test keys
    3.) If pass, returns pass. If fails, return fail

    4.) Check to make sure GOOGLE keys are inplace
    5.) If exists, test keys
    6.) If pass, returns pass. If fails, return fail

    7.) No keys, return error
    """
    try:
        MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN
        try:
            address_coded = urllib.parse.quote_plus('Flinders Street Melbourne')
            print(address_coded)
            url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + address_coded + '.json?access_token=' + settings.MAPBOX_API_TOKEN
            if url.lower().startswith('http'):
                req = urllib.request.Request(url)
            else:
                raise ValueError from None
            with urllib.request.urlopen(req) as (response):
                data = json.load(response)
            longatude = data['features'][0]['center'][0]
            latitude = data['features'][0]['center'][1]
        except:
            return HttpResponseBadRequest('Sorry, could not contact Mapbox')

    except:
        try:
            google_maps = GoogleMaps(api_key=(settings.GOOGLE_MAP_API_TOKEN))
            location = google_maps.search(location='Flinders Street Melbourne')
            first_location = location.first()
            ongitude = first_location.lng
            latitude = first_location.lat
        except:
            return HttpResponseBadRequest('Could not contact Google Server')

        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def diagnostic_test_recaptcha(request):
    if request.method == 'POST':
        RECAPTCHA_PUBLIC_KEY = ''
        RECAPTCHA_PRIVATE_KEY = ''
        if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
            RECAPTCHA_PUBLIC_KEY = settings.RECAPTCHA_PUBLIC_KEY
            RECAPTCHA_PRIVATE_KEY = settings.RECAPTCHA_PRIVATE_KEY
        else:
            return HttpResponseBadRequest('Either RECAPTCHA_PUBLIC_KEY or RECAPTCHA_PRIVATE_KEY has not been correctly setup in your settings file.')
            recaptcha_response = request.POST.get('g-recaptcha-response')
            print('RECAPTCHA RESPONSE:' + str(recaptcha_response))
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {'secret':RECAPTCHA_PRIVATE_KEY, 
             'response':recaptcha_response}
            if url.lower().startswith('http'):
                req = urllib.request.Request(url)
            else:
                raise ValueError from None
        with urllib.request.urlopen(req, urllib.parse.urlencode(values).encode('utf8')) as (response):
            result = json.load(response)
        if not result['success']:
            return HttpResponseBadRequest('Failed recaptcha!\n' + str(result))
    t = loader.get_template('NearBeach/blank.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def email(request, location_id, destination):
    permission_results = return_user_permission_level(request, None, 'email')
    if permission_results['email'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))
        if request.method == 'POST':
            form = email_form((request.POST),
              location_id=location_id,
              destination=destination)
            if form.is_valid():
                organisation_email = form.cleaned_data['organisation_email']
                email_quote = form.cleaned_data['email_quote']
                to_email = []
                cc_email = []
                bcc_email = []
                from_email = ''
                current_user = User.objects.get(id=(request.user.id))
                if current_user.email == '':
                    from_email = settings.EMAIL_HOST_USER
    else:
        from_email = current_user.email
    if organisation_email:
        to_email.append(organisation_email)
    for row in form.cleaned_data['to_email']:
        to_email.append(row.customer_email)

    for row in form.cleaned_data['cc_email']:
        cc_email.append(row.customer_email)

    for row in form.cleaned_data['bcc_email']:
        bcc_email.append(row.customer_email)

    email = EmailMultiAlternatives((form.cleaned_data['email_subject']),
      (form.cleaned_data['email_content']),
      from_email,
      to_email,
      bcc_email,
      cc=cc_email,
      reply_to=[
     'nearbeach@tpg.com.au'])
    email.attach_alternative(form.cleaned_data['email_content'], 'text/html')
    if email_quote == True:
        quote_results = quote.objects.get(quote_id=location_id)
        quote_template_id = request.POST.get('quote_template_description')
        print('Quote Template ID: ' + str(quote_template_id))
        url_path = 'http://' + request.get_host() + '/preview_quote/' + str(quote_results.quote_uuid) + '/' + str(quote_template_id) + '/'
        print('URL LOCATION:')
        print(url_path)
        html = HTML(url_path)
        pdf_results = html.write_pdf()
        email.attach('Quote - ' + str(quote_results.quote_id), pdf_results, 'application/pdf')
    email.send(fail_silently=False)
    print(email_content)
    email_content_submit = email_content(email_subject=(form.cleaned_data['email_subject']),
      email_content=(form.cleaned_data['email_content']),
      change_user=(request.user),
      is_private=(form.cleaned_data['is_private']))
    email_content_submit.save()
    for row in form.cleaned_data['to_email']:
        email_contact_submit = email_contact(email_content=email_content_submit,
          to_customer=customer.objects.get(customer_id=(row.customer_id)),
          change_user=(request.user),
          is_private=(form.cleaned_data['is_private']))
        email_contact_submit.save()

    for row in form.cleaned_data['cc_email']:
        email_contact_submit = email_contact(email_content=email_content_submit,
          cc_customer=customer.objects.get(customer_id=(row.customer_id)),
          change_user=(request.user),
          is_private=(form.cleaned_data['is_private']))
        email_contact_submit.save()

    for row in form.cleaned_data['bcc_email']:
        email_contact_submit = email_contact(email_content=email_content_submit,
          bcc_customer=customer.objects.get(customer_id=(row.customer_id)),
          change_user=(request.user),
          is_private=(form.cleaned_data['is_private']))
        email_contact_submit.save()

    if destination == 'organisation':
        email_contact_submit = email_contact(email_content=email_content_submit,
          organisation=organisation.objects.get(organisation_id=location_id),
          change_user=(request.user),
          is_private=(form.cleaned_data['is_private']))
        email_contact_submit.save()
    else:
        if destination == 'project':
            email_contact_submit = email_contact(email_content=email_content_submit,
              project=project.objects.get(project_id=location_id),
              change_user=(request.user),
              is_private=(form.cleaned_data['is_private']))
            email_contact_submit.save()
        else:
            if destination == 'task':
                email_contact_submit = email_contact(email_content=email_content_submit,
                  task=task.objects.get(task_id=location_id),
                  change_user=(request.user),
                  is_private=(form.cleaned_data['is_private']))
                email_contact_submit.save()
            else:
                if destination == 'opportunity':
                    email_contact_submit = email_contact(email_content=email_content_submit,
                      opportunity=opportunity.objects.get(opportunity_id=location_id),
                      change_user=(request.user),
                      is_private=(form.cleaned_data['is_private']))
                    email_contact_submit.save()
                else:
                    if destination == 'quote':
                        email_contact_submit = email_contact(email_content=email_content_submit,
                          quotes=quote.objects.get(quote_id=location_id),
                          change_user=(request.user),
                          is_private=(form.cleaned_data['is_private']))
                        email_contact_submit.save()
                    elif destination == 'organisation':
                        return HttpResponseRedirect(reverse('organisation_information', args={location_id}))
                    elif destination == 'customer':
                        return HttpResponseRedirect(reverse('customer_information', args={location_id}))
                    elif destination == 'project':
                        return HttpResponseRedirect(reverse('project_information', args={location_id}))
                    elif destination == 'task':
                        return HttpResponseRedirect(reverse('task_information', args={location_id}))
                    elif destination == 'opportunity':
                        return HttpResponseRedirect(reverse('opportunity_information', args={location_id}))
                        if destination == 'quote':
                            return HttpResponseRedirect(reverse('quote_information', args={location_id}))
                            return HttpResponseRedirect(reverse('dashboard'))
                        else:
                            print('ERROR with email form.')
                            print(form.errors)
                    else:
                        t = loader.get_template('NearBeach/email.html')
                        quote_template_results = ''
                        if destination == 'organisation':
                            organisation_results = organisation.objects.get(organisation_id=location_id)
                            initial = {'organisation_email': organisation_results.organisation_email}
                        else:
                            if destination == 'customer':
                                customer_results = customer.objects.get(is_deleted='FALSE',
                                  customer_id=location_id)
                                initial = {'to_email': customer_results.customer_id}
                            else:
                                if destination == 'project':
                                    customer_results = customer.objects.filter(customer_id__in=(project_customer.objects.filter(is_deleted='FALSE',
                                      project_id=location_id).values('customer_id')))
                                    print(customer_results)
                                    initial = {'to_email': customer_results}
                                else:
                                    if destination == 'task':
                                        print('Selected TASK')
                                        task_results = task.objects.get(task_id=location_id)
                                        customer_results = customer.objects.filter(is_deleted='FALSE',
                                          customer_id__in=(task_customer.objects.filter(is_deleted='FALSE',
                                          task_id=location_id).values('customer_id')))
                                        initial = {'to_email': customer_results}
                                        print(customer_results)
                                    else:
                                        if destination == 'opportunity':
                                            customer_results = customer.objects.filter(Q(is_deleted='FALSE') & Q(Q(customer_id__in=customer.objects.filter(is_deleted='FALSE',
                                              organisation_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                                              opportunity_id=location_id,
                                              organisation_id__isnull=False).values('organisation_id')))) | Q(customer_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                                              customer_id__isnull=False,
                                              opportunity_id=location_id).values('customer_id')))))
                                            initial = {'to_email': customer_results}
                                        else:
                                            if destination == 'quote':
                                                quote_template_results = quote_template.objects.filter(is_deleted='FALSE')
                                                customer_results = customer.objects.filter(is_deleted='FALSE',
                                                  customer_id__in=(quote_responsible_customer.objects.filter(is_deleted='FALSE',
                                                  quote_id=location_id).values('customer_id')))
                                                initial = {'to_email': customer_results}
                                            else:
                                                print('Something went wrong')
                    c = {'email_form':email_form(initial=initial,
                       location_id=location_id,
                       destination=destination),  'destination':destination, 
                     'location_id':location_id, 
                     'new_item_permission':permission_results['new_item'], 
                     'administration_permission':permission_results['administration'], 
                     'quote_template_results':quote_template_results}
                    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def email_history(request, location_id, destination):
    permission_results = return_user_permission_level(request, None, 'email')
    if destination == 'organisation':
        email_results = email_content.objects.filter(is_deleted='FALSE',
          email_content_id__in=(email_contact.objects.filter(Q(is_deleted='FALSE') & Q(organisation_id=location_id) & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
    else:
        if destination == 'customer':
            email_results = email_content.objects.filter(is_deleted='FALSE',
              email_content_id__in=(email_contact.objects.filter((Q(to_customer=location_id) | Q(cc_customer=location_id)) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
        else:
            if destination == 'project':
                email_results = email_content.objects.filter(is_deleted='FALSE',
                  email_content_id__in=(email_contact.objects.filter(Q(project=location_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
            else:
                if destination == 'task':
                    email_results = email_content.objects.filter(is_deleted='FALSE',
                      email_content_id__in=(email_contact.objects.filter(Q(task_id=location_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
                else:
                    if destination == 'opportunity':
                        email_results = email_content.objects.filter(is_deleted='FALSE',
                          email_content_id__in=(email_contact.objects.filter(Q(opportunity_id=location_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
                    else:
                        if destination == 'quote':
                            email_results = email_content.objects.filter(is_deleted='FALSE',
                              email_content_id__in=(email_contact.objects.filter(Q(quotes=location_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
                        else:
                            email_results = ''
    t = loader.get_template('NearBeach/email_history.html')
    print(email_results)
    c = {'destination':destination, 
     'location_id':location_id, 
     'email_results':email_results, 
     'email_permission':permission_results['email']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def email_information(request, email_content_id):
    permission_results = return_user_permission_level(request, None, 'email')
    if permission_results['email'] < 1:
        return HttpResponseRedirect(reverse('permission_denied'))
    email_content_results = email_content.objects.get(is_deleted='FALSE',
      email_content_id=email_content_id)
    to_email_results = email_contact.objects.filter(is_deleted='FALSE',
      email_content_id=email_content_id,
      to_customer__isnull=False)
    cc_email_results = email_contact.objects.filter(is_deleted='FALSE',
      email_content_id=email_content_id,
      cc_customer__isnull=False)
    bcc_email_results = email_contact.objects.filter(is_deleted='FALSE',
      email_content_id=email_content_id,
      bcc_customer__isnull=False)
    if email_content_results.is_private == True:
        if not email_content_results.change_user == request.user:
            return HttpResponseRedirect(reverse('permission_denied'))
    initial = {'email_subject':email_content_results.email_subject,  'email_content':email_content_results.email_content}
    t = loader.get_template('NearBeach/email_information.html')
    c = {'email_content_results':email_content_results, 
     'email_information_form':email_information_form(initial=initial), 
     'to_email_results':to_email_results, 
     'cc_email_results':cc_email_results, 
     'bcc_email_results':bcc_email_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def extract_quote(request, quote_uuid, quote_template_id):
    url_path = 'http://' + request.get_host() + '/preview_quote/' + quote_uuid + '/' + quote_template_id + '/'
    html = HTML(url_path)
    pdf_results = html.write_pdf()
    response = HttpResponse(pdf_results, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="NearBeach Quote.pdf"'
    return response


@login_required(login_url='login', redirect_field_name='')
def extract_requirement(request, requirement_id):
    """
    extract requirement will create a simple DOCX document which the use can use to present to customers/stakeholders.
    :param request:
    :param requirement_id: The requirement ID we will be extracting
    :return: A simple DOCX file.

    Method
    ~~~~~~
    1. Check user permissions
    2. Gather the required data for the requirement, requirement_items
    3. Construct the template and feed into a variable
    4. Construct the document location - usually under /private/
    5. Render the results to DOCX using pypandoc
    6. Return the results to the user as an attachment
    """
    requirement_results = requirement.objects.get(requirement_id=requirement_id)
    requirement_link_results = requirement_link.objects.filter(is_deleted='FALSE',
      requirement_id=requirement_id)
    requirement_item_results = requirement_item.objects.filter(is_deleted='FALSE',
      requirement_id=requirement_id)
    requirement_item_link_results = requirement_item_link.objects.filter(is_deleted='FALSE',
      requirement_item_id__in=(requirement_item_results.values('requirement_item_id')))
    t = loader.get_template('NearBeach/requirement_information/preview_requirement.html')
    c = {'requirement_results':requirement_results, 
     'requirement_link_results':requirement_link_results, 
     'requirement_item_results':requirement_item_results, 
     'requirement_item_link_results':requirement_item_link_results}
    data = HttpResponse(t.render(c, request))
    file_name = 'requirement_' + str(requirement_id) + '_' + str(datetime.datetime.now()) + '.docx'
    outfile = settings.PRIVATE_MEDIA_ROOT + file_name
    output = pypandoc.convert_text((data.content),
      format='html',
      to='docx',
      outputfile=outfile,
      extra_args=[
     '-M2GB',
     '+RTS',
     '-K64m',
     '-RTS'])
    return server.serve(request, path=outfile)


@login_required(login_url='login', redirect_field_name='')
def group_information(request, group_id):
    """
    This def will bring up the group information page. If the user makes a change then it will apply those changes.
    This is assuming that the group_id is not the ADMINISTRATION page - because we do not want to change there AT ALL!!
    :param request:
    :param group_id:
    :return:
    """
    permission_results = return_user_permission_level(request, None, ['administration'])
    if permission_results['administration'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    else:
        group_results = group.objects.get(group_id=group_id)
        if group_id == 1 or group_id == '1':
            group_form_results = None
        else:
            group_form_results = group_form(group_id=group_id,
              initial={'group_name':group_results.group_name, 
             'parent_group':group_results.parent_group})
    t = loader.get_template('NearBeach/administration/group_information.html')
    c = {'group_form':group_form_results, 
     'group_id':group_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def index(request):
    """
        The index page determines if a particular user has logged in. It will
        follow the following steps
        
        Method
        ~~~~~~
        1.) If there is a user logged in, if not, send them to login
        2.) Find out if this user should be in the system, if not send them to
                invalid view
        3.) If survived this far the user will be sent to "Active Projects"
        """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('dashboard'))
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login', redirect_field_name='')
def kanban_board_close(request, kanban_board_id):
    if request.method == 'POST':
        kanban_update = kanban_board.objects.get(kanban_board_id=kanban_board_id)
        kanban_update.kanban_board_status = 'Closed'
        kanban_update.save()
        return HttpResponseRedirect(reverse('search_kanban'))
    return HttpResponseBadRequest('Sorry, this request can only be done in post')


@login_required(login_url='login', redirect_field_name='')
def kanban_edit_card(request, kanban_card_id):
    kanban_card_results = kanban_card.objects.get(kanban_card_id=kanban_card_id)
    if not kanban_card_results.project:
        if kanban_card_results.task or kanban_card_results.requirement:
            linked_card = True
    else:
        linked_card = False
    permission_results = return_user_permission_level(request, None, ['kanban', 'kanban_card', 'kanban_comment'])
    if permission_results['kanban'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
        if request.method == 'POST' and permission_results['kanban'] > 1:
            form = kanban_card_form((request.POST),
              kanban_board_id=(kanban_card_results.kanban_board_id))
            if form.is_valid():
                kanban_card_instance = kanban_card.objects.get(kanban_card_id=kanban_card_id)
                current_user = request.user
                kanban_column_extract = form.cleaned_data['kanban_column']
                kanban_level_extract = form.cleaned_data['kanban_level']
                if linked_card == False:
                    kanban_card_instance.kanban_card_text = form.cleaned_data['kanban_card_text']
                kanban_card_instance.kanban_column_id = kanban_column_extract.kanban_column_id
                kanban_card_instance.kanban_level_id = kanban_level_extract.kanban_level_id
                kanban_card_instance.save()
                kanban_comment_extract = form.cleaned_data['kanban_card_comment']
                if not kanban_comment_extract == '':
                    kanban_comment_submit = kanban_comment(kanban_card_id=(kanban_card_instance.kanban_card_id),
                      kanban_comment=kanban_comment_extract,
                      user_id=current_user,
                      user_infomation=(current_user.id),
                      change_user=(request.user))
                    kanban_comment_submit.save()
                t = loader.get_template('NearBeach/kanban/kanban_card_information.html')
                c = {'kanban_card_submit': kanban_comment_extract}
    else:
        print(form.errors)
        HttpResponseBadRequest(form.errors)
    kanban_comment_results = kanban_comment.objects.filter(kanban_card_id=kanban_card_id)
    t = loader.get_template('NearBeach/kanban/kanban_edit_card.html')
    c = {'kanban_card_form':kanban_card_form(kanban_board_id=kanban_card_results.kanban_board_id,
       instance=kanban_card_results), 
     'kanban_permission':permission_results['kanban'], 
     'kanban_card_permission':permission_results['kanban_card'], 
     'kanban_comment_permission':permission_results['kanban_comment'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'kanban_comment_results':kanban_comment_results, 
     'kanban_card_id':kanban_card_id, 
     'linked_card':linked_card, 
     'kanban_card_results':kanban_card_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def kanban_edit_xy_name(request, location_id, destination):
    """
    This function is for editing both kanban column and level names.
    PERMISSIONS WILL NEED TO BE ADDED!
    """
    if destination == 'column':
        kanban_xy_name = kanban_column.objects.get(kanban_column_id=location_id).kanban_column_name.encode('utf8')
    else:
        if destination == 'level':
            kanban_xy_name = kanban_level.objects.get(kanban_level_id=location_id).kanban_level_name.decode('utf8')
        else:
            kanban_xy_name = ''
    t = loader.get_template('NearBeach/kanban/kanban_edit_xy_name.html')
    c = {'kanban_edit_xy_name_form': kanban_edit_xy_name_form(initial={'kanban_xy_name': kanban_xy_name})}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def kanban_information(request, kanban_board_id):
    permission_results = return_user_permission_level(request, None, ['kanban'])
    if permission_results['kanban'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    if permission_results['kanban'] == 1:
        return HttpResponseRedirect(reverse('kanban_read_only', args={kanban_board_id}))
    object_access = object_assignment.objects.filter(is_deleted='FALSE',
      kanban_board_id=kanban_board_id,
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id')))
    if object_access.count() == 0:
        if not permission_results['administration'] == 4:
            return HttpResponseRedirect(reverse('permission_denied'))
    kanban_board_results = kanban_board.objects.get(kanban_board_id=kanban_board_id)
    if kanban_board_results.requirement_id:
        return HttpResponseRedirect(reverse('kanban_requirement_information', args={kanban_board_id}))
    kanban_level_results = kanban_level.objects.filter(is_deleted='FALSE',
      kanban_board=kanban_board_id).order_by('kanban_level_sort_number')
    kanban_column_results = kanban_column.objects.filter(is_deleted='FALSE',
      kanban_board=kanban_board_id).order_by('kanban_column_sort_number')
    kanban_card_results = kanban_card.objects.filter(is_deleted='FALSE',
      kanban_board=kanban_board_id).order_by('kanban_card_sort_number')
    t = loader.get_template('NearBeach/kanban_information.html')
    c = {'kanban_board_id':kanban_board_id, 
     'kanban_board_results':kanban_board_results, 
     'kanban_level_results':kanban_level_results, 
     'kanban_column_results':kanban_column_results, 
     'kanban_card_results':kanban_card_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


def kanban_move_card(request, kanban_card_id, kanban_column_id, kanban_level_id):
    if request.method == 'POST':
        kanban_card_result = kanban_card.objects.get(kanban_card_id=kanban_card_id)
        kanban_card_result.kanban_column_id = kanban_column.objects.get(kanban_column_id=kanban_column_id)
        kanban_card_result.kanban_level_id = kanban_level.objects.get(kanban_level_id=kanban_level_id)
        kanban_card_result.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('This request can only be through POST')


@login_required(login_url='login', redirect_field_name='')
def kanban_new_card(request, kanban_board_id):
    permission_results = return_user_permission_level(request, None, ['kanban'])
    if permission_results['kanban'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = kanban_card_form((request.POST), kanban_board_id=kanban_board_id)
        if form.is_valid():
            kanban_column_results = form.cleaned_data['kanban_column']
            kanban_level_results = form.cleaned_data['kanban_level']
            max_value_results = kanban_card.objects.filter(kanban_column=(kanban_column_results.kanban_column_id),
              kanban_level=(kanban_level_results.kanban_level_id)).aggregate(Max('kanban_card_sort_number'))
            try:
                max_value = max_value_results['kanban_card_sort_number__max'] + 1
            except:
                max_value = 0

            kanban_card_submit = kanban_card(kanban_card_text=(form.cleaned_data['kanban_card_text']),
              kanban_column=kanban_column_results,
              kanban_level=kanban_level_results,
              change_user=(request.user),
              kanban_card_sort_number=max_value,
              kanban_board_id=kanban_board_id)
            kanban_card_submit.save()
            t = loader.get_template('NearBeach/kanban/kanban_card_information.html')
            c = {'kanban_card_submit': kanban_card_submit}
            return HttpResponse(t.render(c, request))
        print(form.errors)
    kanban_column_results = kanban_column.objects.filter(kanban_board=kanban_board_id)
    kanban_level_results = kanban_level.objects.filter(kanban_board=kanban_board_id)
    t = loader.get_template('NearBeach/kanban/kanban_new_card.html')
    c = {'kanban_column_results':kanban_column_results, 
     'kanban_level_results':kanban_level_results, 
     'kanban_card_form':kanban_card_form(kanban_board_id=kanban_board_id), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'kanban_board_id':kanban_board_id}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def kanban_new_link(request, kanban_board_id, location_id='', destination=''):
    permission_results = return_user_permission_level(request, None, ['kanban'])
    if permission_results['kanban'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = kanban_new_link_form((request.POST),
          kanban_board_id=kanban_board_id)
        if form.is_valid():
            if kanban_card.objects.filter(project_id=location_id, is_deleted='FALSE'):
                if not (destination == 'project' or kanban_card.objects.filter(task_id=location_id, is_deleted='FALSE') and destination == 'task'):
                    if not kanban_card.objects.filter(requirement_id=location_id, is_deleted='FALSE') or destination == 'requirement':
                        return HttpResponseBadRequest('Card already exists')
            else:
                kanban_column = form.cleaned_data['kanban_column']
                kanban_level = form.cleaned_data['kanban_level']
                max_value_results = kanban_card.objects.filter(kanban_column=(kanban_column.kanban_column_id),
                  kanban_level=(kanban_level.kanban_level_id)).aggregate(Max('kanban_card_sort_number'))
                try:
                    max_value = max_value_results['kanban_card_sort_number__max'] + 1
                except:
                    max_value = 0

                kanban_card_submit = kanban_card(change_user=(request.user),
                  kanban_column=kanban_column,
                  kanban_level=kanban_level,
                  kanban_card_sort_number=max_value,
                  kanban_board=kanban_board.objects.get(kanban_board_id=kanban_board_id))
                if destination == 'project':
                    kanban_card_submit.project = project.objects.get(project_id=location_id)
                    kanban_card_submit.kanban_card_text = 'PRO' + location_id + ' - ' + kanban_card_submit.project.project_name
                else:
                    if destination == 'task':
                        kanban_card_submit.task = task.objects.get(task_id=location_id)
                        kanban_card_submit.kanban_card_text = 'TASK' + location_id + ' - ' + kanban_card_submit.task.task_short_description
                    else:
                        if destination == 'requirement':
                            kanban_card_submit.requirement = requirement.objects.get(requirement_id=location_id)
                            kanban_card_submit.kanban_card_text = 'REQ' + location_id + ' - ' + kanban_card_submit.requirement.requirement_title
                        else:
                            return HttpResponseBadRequest('Sorry, that type of destination does not exist')
            kanban_card_submit.save()
            t = loader.get_template('NearBeach/kanban/kanban_card_information.html')
            c = {'kanban_card_submit': kanban_card_submit}
            return HttpResponse(t.render(c, request))
        print(form.errors)
        return HttpResponseBadRequest('BAD FORM')
    kanban_card_results = kanban_card.objects.filter(is_deleted='FALSE',
      kanban_board_id=kanban_board_id)
    project_results = project.objects.filter(is_deleted='FALSE',
      project_status__in=('Backlog', 'Blocked', 'In Progress', 'Test/Review')).exclude(project_id__in=(kanban_card_results.filter(project_id__isnull=False).values('project_id')))
    task_results = task.objects.filter(is_deleted='FALSE',
      task_status__in=('Backlog', 'Blocked', 'In Progress', 'Test/Review')).exclude(task_id__in=(kanban_card_results.filter(task_id__isnull=False).values('task_id')))
    requirement_results = requirement.objects.filter(is_deleted='FALSE',
      requirement_status_id__in=(list_of_requirement_status.objects.filter(requirement_status_is_closed='FALSE').values('requirement_status_id'))).exclude(is_deleted='FALSE',
      requirement_id__in=(kanban_card_results.filter(requirement_id__isnull=False).values('requirement_id')))
    t = loader.get_template('NearBeach/kanban/kanban_new_link.html')
    c = {'project_results':project_results, 
     'task_results':task_results, 
     'requirement_results':requirement_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'kanban_new_link_form':kanban_new_link_form(kanban_board_id=kanban_board_id)}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def kanban_properties(request, kanban_board_id):
    print('Kanban Properties')
    permission_results = return_user_permission_level(request, None, ['kanban'])
    if permission_results['kanban'] < 4:
        return HttpResponseRedirect(reverse('permission_denied'))
    kanban_board_results = kanban_board.objects.get(kanban_board_id=kanban_board_id)
    if kanban_board_results.requirement:
        print('Sorry, can not edit these')
        return HttpResponseBadRequest('Sorry, but users are not permitted to edit a Requirement Kanban Board.')
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        kanban_board_results.kanban_board_name = str(received_json_data['kanban_board_name'])
        kanban_board_results.save()
        print('["columns"]["length"]')
        print(received_json_data['columns']['length'])
        for row in range(0, received_json_data['columns']['length']):
            kanban_column_update = kanban_column.objects.get(kanban_column_id=(received_json_data['columns'][str(row)]['id']))
            kanban_column_update.kanban_column_sort_number = row
            kanban_column_update.kanban_column_name = received_json_data['columns'][str(row)]['title']
            kanban_column_update.save()

        for row in range(0, received_json_data['levels']['length']):
            kanban_level_update = kanban_level.objects.get(kanban_level_id=(received_json_data['levels'][str(row)]['id']))
            kanban_level_update.kanban_level_sort_number = row
            kanban_level_update.kanban_level_name = received_json_data['levels'][str(row)]['title']
            kanban_level_update.save()

        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    kanban_column_results = kanban_column.objects.filter(is_deleted='FALSE',
      kanban_board_id=kanban_board_id).order_by('kanban_column_sort_number')
    kanban_level_results = kanban_level.objects.filter(is_deleted='FALSE',
      kanban_board_id=kanban_board_id).order_by('kanban_level_sort_number')
    t = loader.get_template('NearBeach/kanban/kanban_properties.html')
    c = {'kanban_board_id':kanban_board_id, 
     'kanban_column_results':kanban_column_results, 
     'kanban_level_results':kanban_level_results, 
     'kanban_board_results':kanban_board_results, 
     'kanban_properties_form':kanban_properties_form(initial={'kanban_board_name': kanban_board_results.kanban_board_name}), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'permission':permission_results['kanban']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def kanban_read_only(request, kanban_board_id):
    permission_results = return_user_permission_level(request, None, ['kanban'])
    print(permission_results)
    if permission_results['kanban'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    kanban_board_results = kanban_board.objects.get(kanban_board_id=kanban_board_id)
    if kanban_board_results.requirement_id:
        return HttpResponseRedirect(reverse('kanban_requirement_information', args={kanban_board_id}))
    kanban_level_results = kanban_level.objects.filter(is_deleted='FALSE',
      kanban_board=kanban_board_id).order_by('kanban_level_sort_number')
    kanban_column_results = kanban_column.objects.filter(is_deleted='FALSE',
      kanban_board=kanban_board_id).order_by('kanban_column_sort_number')
    kanban_card_results = kanban_card.objects.filter(is_deleted='FALSE',
      kanban_board=kanban_board_id).order_by('kanban_card_sort_number')
    t = loader.get_template('NearBeach/kanban/kanban_read_only.html')
    c = {'kanban_board_id':kanban_board_id, 
     'kanban_board_results':kanban_board_results, 
     'kanban_level_results':kanban_level_results, 
     'kanban_column_results':kanban_column_results, 
     'kanban_card_results':kanban_card_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def kanban_requirement_information(request, kanban_board_id):
    permission_results = return_user_permission_level(request, None, ['kanban'])
    if permission_results['kanban'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    else:
        kanban_board_results = kanban_board.objects.get(kanban_board_id=kanban_board_id)
        return kanban_board_results.requirement_id or HttpResponseRedirect(reverse('kanban_information', args={kanban_board_id}))
    object_access = object_assignment.objects.filter(is_deleted='FALSE',
      requirement_id=(kanban_board_results.requirement_id),
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id')))
    if object_access.count() == 0:
        if not permission_results['administration'] == 4:
            return HttpResponseRedirect(reverse('permission_denied'))
    requirement_id = kanban_board_results.requirement_id
    requirement_results = requirement.objects.get(requirement_id=requirement_id)
    requirement_item_results = requirement_item.objects.filter(is_deleted='FALSE',
      requirement_id=requirement_id)
    item_status_results = list_of_requirement_item_status.objects.filter(is_deleted='FALSE')
    t = loader.get_template('NearBeach/kanban_requirement_information.html')
    c = {'requirement_id':requirement_id, 
     'requirement_results':requirement_results, 
     'requirement_item_results':requirement_item_results, 
     'item_status_results':item_status_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'permission':permission_results['kanban']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def kanban_requirement_item_update(request, requirement_item_id, status_id):
    if request.method == 'POST':
        requirement_item_update = requirement_item.objects.get(requirement_item_id=requirement_item_id)
        requirement_item_update.requirement_item_status = list_of_requirement_item_status.objects.get(requirement_item_status_id=status_id)
        requirement_item_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, but this is a POST request only')


def kudos_rating(request, kudos_key):
    if request.method == 'POST':
        form = kudos_form(request.POST)
        if form.is_valid():
            kudos_update = kudos.objects.get(kudos_key=kudos_key)
            kudos_update.kudos_rating = form.cleaned_data['kudos_rating']
            kudos_update.improvement_note = form.cleaned_data['improvement_note']
            kudos_update.liked_note = form.cleaned_data['liked_note']
            kudos_update.change_user = request.user
            kudos_update.submitted_kudos = 'TRUE'
            kudos_update.save()
            t = loader.get_template('NearBeach/kudos_thank_you.html')
            c = {}
            return HttpResponse(t.render(c, request))
    else:
        print(form.errors)
        return HttpResponseBadRequest('Form had errors within it. It failed')
        kudos_results = kudos.objects.get(kudos_key=kudos_key)
        project_results = project.objects.get(project_id=(kudos_results.project_id))
        if kudos_results.submitted_kudos == 'TRUE':
            t = loader.get_template('NearBeach/kudos_read_only.html')
        else:
            t = loader.get_template('NearBeach/kudos_rating.html')
    c = {'kudos_form':kudos_form(initial={'project_description':project_results.project_description, 
      'kudos_rating':2}), 
     'kudos_key':kudos_key, 
     'project_results':project_results}
    return HttpResponse(t.render(c, request))


def kudos_read_only(request, kudos_key):
    kudos_results = kudos.objects.get(kudos_key=kudos_key)
    project_results = project.objects.get(project_id=(kudos_results.project_id))
    t = loader.get_template('NearBeach/kudos_read_only.html')
    c = {'kudos_read_only_form':kudos_read_only_form(initial={'project_description':project_results.project_description, 
      'improvement_note':kudos_results.improvement_note, 
      'liked_note':kudos_results.liked_note}), 
     'kudos_key':kudos_key, 
     'kudos_results':kudos_results, 
     'star_range':range(kudos_results.kudos_rating), 
     'project_results':project_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def list_of_tags(request):
    """
    List of tags will allow a user to configure all the tags currently in NearBeach. The user will be able to
    - Merge tags together
    - Delete tags
    - Rename tags
    - Create new tags
    :param request:
    :return: Page of tags

    Method
    ~~~~~~
    1. Check user permissions - if they are not allowed here send them to the naughty corner
    """
    permission_results = return_user_permission_level(request, None, 'tag')
    if permission_results['tag'] < 1:
        return HttpResponseRedirect(reverse(permission_denied))
    tag_results = tag.objects.filter(is_deleted='FALSE')
    t = loader.get_template('NearBeach/tags/list_of_tags.html')
    c = {'tag_results':tag_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


def login(request):
    """
        For some reason I can not use the varable "login_form" here as it is already being used.
        Instead I will use the work form.
        
        The form is declared at the start and filled with either the POST data OR nothing. If this
        process is called in POST, then the form will be checked and if it passes the checks, the
        user will be logged in.
        
        If the form is not in POST (aka GET) OR fails the checks, then it will create the form with
        the relevant errors.
        """
    form = login_form(request.POST or None)
    print('LOGIN REQUEST')
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''
    if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY'):
        if hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
            RECAPTCHA_PUBLIC_KEY = settings.RECAPTCHA_PUBLIC_KEY
            RECAPTCHA_PRIVATE_KEY = settings.RECAPTCHA_PRIVATE_KEY
    elif request.method == 'POST':
        print('POST')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print('DATA EXTRACTED')
            if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {'secret':RECAPTCHA_PRIVATE_KEY, 
                 'response':recaptcha_response}
                if url.lower().startswith('http'):
                    req = urllib.request.Request(url)
                else:
                    raise ValueError from None
                with urllib.request.urlopen(req, urllib.parse.urlencode(values).encode('utf8')) as (response):
                    result = json.load(response)
                if result['success']:
                    user = auth.authenticate(username=username, password=password)
                    auth.login(request, user)
            else:
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
            if request.user.is_authenticated:
                print('User Authenticated')
                if not permission_set.objects.all():
                    submit_permission_set = permission_set(permission_set_name='Administration Permission Set',
                      administration_assign_user_to_group=4,
                      administration_create_group=4,
                      administration_create_permission_set=4,
                      administration_create_user=4,
                      assign_campus_to_customer=4,
                      associate_project_and_task=4,
                      bug=4,
                      bug_client=4,
                      customer=4,
                      email=4,
                      invoice=4,
                      invoice_product=4,
                      kanban=4,
                      kanban_card=4,
                      opportunity=4,
                      organisation=4,
                      organisation_campus=4,
                      project=4,
                      quote=4,
                      requirement=4,
                      requirement_link=4,
                      tag=4,
                      task=4,
                      tax=4,
                      template=4,
                      whiteboard=4,
                      document=1,
                      contact_history=1,
                      kanban_comment=1,
                      project_history=1,
                      task_history=1,
                      change_user=(request.user))
                    submit_permission_set.save()
                    submit_group = group(group_name='Administration',
                      change_user=(request.user))
                    submit_group.save()
                    submit_user_group = user_group(username=(request.user),
                      group=group.objects.get(group_id=1),
                      permission_set=permission_set.objects.get(permission_set_id=1),
                      change_user=(request.user))
                    submit_user_group.save()
                request.session['is_superuser'] = request.user.is_superuser
                return HttpResponseRedirect(reverse('alerts'))
            print('User not authenticated')
        else:
            print(form.errors)
    background_image = 'NearBeach/images/NearBeach_Background_%(number)03d.webp' % {'number': random.randint(1, 19)}
    t = loader.get_template('NearBeach/login.html')
    c = {'login_form':form, 
     'RECAPTCHA_PUBLIC_KEY':RECAPTCHA_PUBLIC_KEY, 
     'background_image':background_image}
    return HttpResponse(t.render(c, request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login', redirect_field_name='')
def merge_tags(request, old_tag_id, new_tag_id=''):
    """
    Merge tags will get the old tag_id, and update all the tag assoications with the new tag_id before deleting the old
    tag id.
    :param request:
    :param old_tag_id: The old tag that we want to merge
    :param new_tag_id: The new tag that we want to merge into
    :return: back to the tag list

    Method
    ~~~~~~
    1. Check permissions - only a user with a permission of 4 is permitted. Anyone else is sent to the naughty space
    2. Check to see if method is POST - if it check instructions there
    3. Get a list of ALL tags excluding the current old_tag_id
    4. Render out the page and wait for the user
    """
    permission_results = return_user_permission_level(request, None, 'tag')
    if permission_results['tag'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        new_tag_instance = tag.objects.get(tag_id=new_tag_id)
        update_tag_association = tag_assignment.objects.filter(is_deleted='FALSE',
          tag_id=old_tag_id).update(tag_id=new_tag_instance)
        old_tag_instance = tag.objects.get(tag_id=old_tag_id)
        old_tag_instance.is_deleted = 'TRUE'
        old_tag_instance.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    tag_results = tag.objects.filter(is_deleted='FALSE').exclude(tag_id=old_tag_id)
    t = loader.get_template('NearBeach/tags/merge_tags.html')
    c = {'tag_results':tag_results, 
     'old_tag_id':old_tag_id}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def my_profile(request):
    permission_results = return_user_permission_level(request, None, '')
    about_user_results = about_user.objects.filter(is_deleted='FALSE',
      user=(request.user)).order_by('-date_created')
    if about_user_results:
        about_user_text = about_user_results[0].about_user_text
    else:
        about_user_text = ''
    user_instance = User.objects.get(id=(request.user.id))
    if request.method == 'POST':
        form = my_profile_form(request.POST)
        if form.is_valid():
            user_instance.first_name = form.cleaned_data['first_name']
            user_instance.last_name = form.cleaned_data['last_name']
            user_instance.email = form.cleaned_data['email']
            user_instance.save()
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                user_instance = password1 == '' or User.objects.get(id=(request.user.id))
                user_instance.set_password(password1)
                user_instance.save()
    else:
        print(form.errors)
    form = about_user_form(request.POST)
    if form.is_valid() and not about_user_text == form.cleaned_data['about_user_text']:
        if not about_user_text == None:
            about_user_text = form.cleaned_data['about_user_text']
            about_user_submit = about_user(change_user=(request.user),
              about_user_text=about_user_text,
              user_id=(request.user.id))
            about_user_submit.save()
        else:
            print(form.errors)
    project_results = project.objects.filter(is_deleted='FALSE',
      project_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      assigned_user=(request.user.id)).values('project_id').distinct()))
    t = loader.get_template('NearBeach/my_profile.html')
    c = {'project_results':project_results, 
     'my_profile_form':my_profile_form(instance=user_instance), 
     'about_user_form':about_user_form(initial={'about_user_text': about_user_text}), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_bug_client(request):
    permission_results = return_user_permission_level(request, None, 'bug_client')
    if permission_results['bug_client'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
        form_errors = ''
        form = bug_client_form(None or request.POST)
        if request.method == 'POST':
            if form.is_valid():
                bug_client_name = form.cleaned_data['bug_client_name']
                list_of_bug_client = form.cleaned_data['list_of_bug_client']
                bug_client_url = form.cleaned_data['bug_client_url']
                try:
                    url = bug_client_url + list_of_bug_client.bug_client_api_url + 'version'
                    if url.lower().startswith('http'):
                        req = urllib.request.Request(url)
                    else:
                        raise ValueError from None
                    with urllib.request.urlopen(req) as (response):
                        data = json.load(response)
                    bug_client_submit = bug_client(bug_client_name=bug_client_name,
                      list_of_bug_client=list_of_bug_client,
                      bug_client_url=bug_client_url,
                      change_user=(request.user))
                    bug_client_submit.save()
                    return HttpResponseRedirect(reverse('bug_client_list'))
                except:
                    form_errors = 'Could not connect to the API'

    else:
        print(form.errors)
        form_errors = form.errors
    t = loader.get_template('NearBeach/new_bug_client.html')
    c = {'bug_client_form':form, 
     'form_errors':form_errors, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_campus(request, location_id, destination):
    permission_results = return_user_permission_level(request, None, 'organisation_campus')
    if permission_results['organisation_campus'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    else:
        return request.user.is_authenticated or HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        print('\n\nPOST REQUEST')
        print(request.POST)
        print('\n\nEND POST REQUEST')
        form = new_campus_form(request.POST)
        if form.is_valid():
            region_instance = list_of_country_region.objects.get(region_id=(request.POST.get('country_and_regions')))
            campus_nickname = form.cleaned_data['campus_nickname']
            campus_phone = request.POST.get('hidden_campus_phone')
            campus_fax = request.POST.get('hidden_campus_fax')
            campus_address1 = form.cleaned_data['campus_address1']
            campus_address2 = form.cleaned_data['campus_address2']
            campus_address3 = form.cleaned_data['campus_address3']
            campus_suburb = form.cleaned_data['campus_suburb']
            submit_form = campus(campus_nickname=campus_nickname,
              campus_phone=campus_phone,
              campus_fax=campus_fax,
              campus_address1=campus_address1,
              campus_address2=campus_address2,
              campus_address3=campus_address3,
              campus_suburb=campus_suburb,
              campus_region_id=region_instance,
              campus_country_id=(region_instance.country_id),
              change_user=(request.user))
            if destination == 'organisation':
                submit_form.organisation_id = organisation.objects.get(organisation_id=location_id)
            else:
                submit_form.customer = customer.objects.get(customer_id=location_id)
            submit_form.save()
            update_coordinates(submit_form.campus_id)
            if destination == 'organisation':
                return HttpResponseRedirect(reverse(organisation_information, args={location_id}))
            return HttpResponseRedirect(reverse(customer_information, args={location_id}))
        else:
            print(form.errors)
            return HttpResponseRedirect(reverse(new_campus, args={location_id, destination}))
    countries_results = list_of_country.objects.all().order_by('country_name')
    countries_regions_results = list_of_country_region.objects.all().order_by('region_name')
    t = loader.get_template('NearBeach/new_campus.html')
    c = {'location_id':location_id, 
     'destination':destination, 
     'new_campus_form':new_campus_form(), 
     'countries_results':countries_results, 
     'countries_regions_results':countries_regions_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_change_task(request, rfc_id):
    """
    This form is called when;
    - A user wants to create a new change task
    - A user submites a new change task
    :param request:
    :param rfc_id: This will link this change task to the current rfc
    :return: Web page

    Method
    ~~~~~~
    1. Check permissions
    2. Check to see if method is POST - if POST then follow instructions there
    3. Get form data
    4. Get template
    5. Render all that and send to the user
    """
    permission_results = return_user_permission_level(request, None, 'request_for_change')
    if permission_results['request_for_change'] <= 1:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = new_change_task_form((request.POST), rfc_id=rfc_id)
        if form.is_valid():
            start_date = form.cleaned_data['change_task_start_date']
            end_date = form.cleaned_data['change_task_end_date']
            deltaSeconds = (end_date - start_date).total_seconds()
            change_task_submit = change_task(change_task_title=(form.cleaned_data['change_task_title']),
              change_task_start_date=(form.cleaned_data['change_task_start_date']),
              change_task_end_date=(form.cleaned_data['change_task_end_date']),
              change_task_assigned_user=(form.cleaned_data['change_task_assigned_user']),
              change_task_qa_user=(form.cleaned_data['change_task_qa_user']),
              change_task_description=(form.cleaned_data['change_task_description']),
              change_task_required_by=(form.cleaned_data['change_task_required_by']),
              change_user=(request.user),
              change_task_status=1,
              request_for_change=request_for_change.objects.get(rfc_id=rfc_id),
              change_task_seconds=deltaSeconds)
            change_task_submit.save()
            return HttpResponseRedirect(reverse('request_for_change_draft', args={rfc_id}))
        print(form.errors)
    t = loader.get_template('NearBeach/request_for_change/change_task_new.html')
    c = {'rfc_id':rfc_id, 
     'new_change_task_form':new_change_task_form(rfc_id=rfc_id)}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_customer(request, organisation_id):
    permission_results = return_user_permission_level(request, None, 'customer')
    if permission_results['customer'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    form_errors = ''
    if request.method == 'POST':
        form = new_customer_form(request.POST)
        if form.is_valid():
            customer_title = form.cleaned_data['customer_title']
            customer_first_name = form.cleaned_data['customer_first_name']
            customer_last_name = form.cleaned_data['customer_last_name']
            customer_email = form.cleaned_data['customer_email']
            organisation_id = form.cleaned_data['organisation_id']
            submit_form = customer(customer_title=customer_title,
              customer_first_name=customer_first_name,
              customer_last_name=customer_last_name,
              customer_email=customer_email,
              organisation_id=organisation_id,
              change_user=(request.user))
            submit_form.save()
            return HttpResponseRedirect(reverse(customer_information, args={submit_form.customer_id}))
        form_errors = form.errors
    else:
        initial = {'organisation_id': organisation_id}
        form = new_customer_form(initial=initial)
    t = loader.get_template('NearBeach/new_customer.html')
    c = {'new_customer_form':form, 
     'organisation_id':organisation_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'form_errors':form_errors}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_group(request):
    """
    You need to create a new group. You must be over 3 on your administration create group :)
    :param request:
    :return: group_infomration page if in POST or new_group page in GET
    """
    permission_results = return_user_permission_level(request, [None], ['administration_create_group'])
    if permission_results['administration_create_group'] <= 1:
        return HttpResponseRedirect(reverse(permission_denied))
    if request.method == 'POST':
        form = new_group_form(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            group_results = group.objects.filter(is_deleted='FALSE',
              group_name=group_name)
            if group_results:
                return HttpResponseRedirect(reverse('group_information', args={group_results[0].group_id}))
            group_submit = group(group_name=group_name,
              parent_group=(form.cleaned_data['parent_group']),
              change_user=(request.user))
            group_submit.save()
            return HttpResponseRedirect(reverse('group_information', args={group_submit.group_id}))
        print(form.errors)
    t = loader.get_template('NearBeach/administration/new_group.html')
    c = {'new_group_form':new_group_form(), 
     'administration_permission':permission_results['administration'], 
     'new_item_permission':permission_results['new_item']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_kanban_board(request):
    permission_results = return_user_permission_level(request, None, 'kanban')
    if permission_results['kanban'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = kanban_board_form(request.POST)
        if form.is_valid():
            kanban_board_submit = kanban_board(kanban_board_name=(form.cleaned_data['kanban_board_name']),
              change_user=(request.user))
            kanban_board_submit.save()
            column_count = 1
            for line in form.cleaned_data['kanban_board_column'].split('\n'):
                kanban_column_submit = kanban_column(kanban_column_name=line,
                  kanban_column_sort_number=column_count,
                  kanban_board=kanban_board_submit,
                  change_user=(request.user))
                kanban_column_submit.save()
                column_count = column_count + 1

            level_count = 1
            for line in form.cleaned_data['kanban_board_level'].split('\n'):
                kanban_level_submit = kanban_level(kanban_level_name=line,
                  kanban_level_sort_number=level_count,
                  kanban_board=kanban_board_submit,
                  change_user=(request.user))
                kanban_level_submit.save()
                level_count = level_count + 1

            select_groups = form.cleaned_data['select_groups']
            for row in select_groups:
                group_instance = group.objects.get(group_name=row)
                permission_save = object_assignment(kanban_board_id=kanban_board_submit,
                  group_id=group_instance,
                  change_user=(request.user))
                permission_save.save()

            return HttpResponseRedirect(reverse('kanban_information', args={kanban_board_submit.kanban_board_id}))
        print(form.errors)
        return HttpResponseBadRequest(form.errors)
    t = loader.get_template('NearBeach/new_kanban_board.html')
    c = {'kanban_board_form':kanban_board_form(initial={'kanban_board_column':'Backlog\nBlocked\nIn Progress\nCompleted', 
      'kanban_board_level':'Sprint 1\nSprint 2'}), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_kanban_requirement_board(request, requirement_id):
    permission_results = return_user_permission_level(request, None, 'kanban')
    if permission_results['kanban'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    requirement_instance = requirement.objects.get(requirement_id=requirement_id)
    kanban_board_submit = kanban_board(kanban_board_name=(requirement_instance.requirement_title),
      requirement=requirement_instance,
      change_user=(request.user))
    kanban_board_submit.save()
    return HttpResponseRedirect(reverse('kanban_requirement_information',
      args={
     kanban_board_submit.kanban_board_id}))


@login_required(login_url='login', redirect_field_name='')
def new_kudos(request, project_id):
    """
    Method
    ~~~~~~
    1. Do checks to see if user is allowed to do this
    2. Find ALL customers associated with this project
    3. Create a new kudos for each customer
    4. Go back to read only
    :param request: -- basic
    :param project_id: the project that we will be creating kudos for
    :return: back to the read only
    """
    permission_results = return_user_permission_level(request, None, 'project')
    print('REQUEST PATH: ' + request.path)
    print('REQUEST PATH INFO: ' + request.path_info)
    print('REQUEST FULL PATH: ' + request.get_full_path())
    print('RAW URI: ' + request.get_raw_uri())
    print('RAW get_host' + request.get_host())
    if permission_results['project'] < 4:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        project_customer_results = project_customer.objects.filter(is_deleted='FALSE',
          project_id=project_id)
        for customer_line in project_customer_results:
            kudos_submit = kudos(kudos_rating=2,
              customer=(customer_line.customer_id),
              project_id=project_id,
              change_user=(request.user))
            kudos_submit.save()
            try:
                EMAIL_HOST_USER = settings.EMAIL_HOST_USER
                EMAIL_BACKEND = settings.EMAIL_BACKEND
                EMAIL_USE_TLS = settings.EMAIL_USE_TLS
                EMAIL_HOST = settings.EMAIL_HOST
                EMAIL_PORT = settings.EMAIL_PORT
                EMAIL_HOST_USER = settings.EMAIL_HOST_USER
                EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
                email_content = 'Hello ' + str(customer_line.customer_id.customer_first_name) + '<br/>We have recently finished working on your project. Can you please evaluate our work at: <a href="' + request.get_host() + '/kudos_rating/' + str(kudos_submit.kudos_key) + '">' + request.get_host() + '/kudos_rating/' + str(kudos_submit.kudos_key) + '/</a><br/>Regards<br/>Project Team'
                email = EmailMultiAlternatives('Kudos Evaluation form', email_content, 'donotreply@nearbeach.org', [
                 customer_line.customer_id.customer_email])
                email.attach_alternative(email_content, 'text/html')
                if not email.send():
                    return HttpResponseBadRequest('Email did not send correctly.')
            except:
                print('Email not sent')

        return HttpResponseRedirect(reverse('project_readonly',
          args={
         project_id}))
    return HttpResponseBadRequest('Sorry, can only do this request through post')


@login_required(login_url='login', redirect_field_name='')
def new_opportunity(request):
    """
    New opportunity will give the user the ability to create a new opportunity. The new opportunity will not be connected
    with any other customers or organisations. This can be done in the opportunity information page.
    :param request:
    :return:
    """
    permission_results = return_user_permission_level(request, None, 'opportunity')
    if permission_results['opportunity'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = new_opportunity_form(request.POST)
        if form.is_valid():
            current_user = request.user
            select_groups = form.cleaned_data['select_groups']
            stage_of_opportunity_instance = list_of_opportunity_stage.objects.get(opportunity_stage_id=(request.POST.get('opportunity_stage')))
            submit_opportunity = opportunity(opportunity_name=(form.cleaned_data['opportunity_name']),
              opportunity_description=(form.cleaned_data['opportunity_description']),
              currency_id=(form.cleaned_data['currency_id']),
              opportunity_amount=(form.cleaned_data['opportunity_amount']),
              amount_type_id=(form.cleaned_data['amount_type_id']),
              opportunity_success_probability=(form.cleaned_data['opportunity_success_probability']),
              lead_source_id=(form.cleaned_data['lead_source_id']),
              opportunity_expected_close_date=(form.cleaned_data['opportunity_expected_close_date']),
              opportunity_stage_id=stage_of_opportunity_instance,
              user_id=(request.user),
              change_user=(request.user))
            submit_opportunity.save()
            for row in select_groups:
                group_instance = group.objects.get(group_name=row)
                permission_save = object_assignment(opportunity_id=submit_opportunity,
                  group_id=group_instance,
                  change_user=(request.user))
                permission_save.save()

            return HttpResponseRedirect(reverse(opportunity_information, args={submit_opportunity.opportunity_id}))
        print(form.errors)
    opportunity_stage_results = list_of_opportunity_stage.objects.all()
    t = loader.get_template('NearBeach/new_opportunity.html')
    c = {'new_opportunity_form':new_opportunity_form(), 
     'timezone':settings.TIME_ZONE, 
     'opportunity_stage_results':opportunity_stage_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_opportunity_link(request, opportunity_id, destination, location_id=''):
    """
    This def will link an object [requirement, project, task] to the opportunity. The GET command will render the search
    function where the POST will apply the link (JavaScript will navigate the user back to the opportunity
    :param request:
    :param opportunity_id: The opportunity we want to apply the link to
    :param destination: The destination [requirement, project, task]
    :param location: The id of the object we are linking
    :return:

    Method
    ~~~~~~
    1. Check user permission - send them to the naughty place if they do not have permissions
    2. Check method to see if it is POST - use method in here if post
    3. Check the destination - obtain those
        - Open objects
        - That the user has access to
    4. Get template
    5. Render
    """
    opportunity_results = opportunity.objects.get(opportunity_id=opportunity_id)
    group_results = group.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      group_id__isnull=False,
      username_id=(request.user)).values('group_id'))).values('group_id')
    permission_results = return_user_permission_level(request, group_results, 'opportunity')
    if permission_results['opportunity'] <= 1:
        return HttpResponseRedirect(reverse('permission_denied'))
    elif request.method == 'POST':
        object_assignment_submit = object_assignment(opportunity_id=opportunity_results,
          change_user=(request.user))
        if destination == 'requirement':
            object_assignment_submit.requirement_id = requirement.objects.get(requirement_id=location_id)
    elif destination == 'project':
        object_assignment_submit.project_id = project.objects.get(project_id=location_id)
    else:
        if destination == 'task':
            object_assignment_submit.task_id = task.objects.get(task_id=location_id)
        else:
            object_assignment_submit.save()
            t = loader.get_template('NearBeach/blank.html')
            c = {}
            return HttpResponse(t.render(c, request))
            if destination == 'requirement':
                search_results = requirement.objects.filter(is_deleted='FALSE',
                  requirement_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                  requirement_id__isnull=False,
                  group_id__in=group_results).values('requirement_id')),
                  requirement_status_id__in=(list_of_requirement_status.objects.filter(is_deleted='FALSE',
                  requirement_status_is_closed='FALSE').values('requirement_status_id')))
            else:
                if destination == 'project':
                    search_results = project.objects.filter(project_status__in=[
                     'Backlog',
                     'Blocked',
                     'In Progress',
                     'Test/Review'],
                      is_deleted='FALSE',
                      project_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                      project_id__isnull=False,
                      group_id__in=group_results).values('project_id')))
                else:
                    if destination == 'task':
                        search_results = task.objects.filter(task_status__in=[
                         'Backlog',
                         'Blocked',
                         'In Progress',
                         'Test/Review'],
                          is_deleted='FALSE',
                          task_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                          task_id__isnull=False,
                          group_id__in=group_results).values('task_id')))
                    else:
                        search_results = None
    t = loader.get_template('NearBeach/opportunity_information/new_opportunity_link.html')
    c = {'destination':destination, 
     'opportunity_id':opportunity_id, 
     'opportunity_results':opportunity_results, 
     'search_results':search_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_organisation(request):
    permission_results = return_user_permission_level(request, None, 'organisation')
    if permission_results['organisation'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
        form_errors = ''
        form = new_organisation_form(request.POST or None)
        duplicate_results = None
        if request.method == 'POST':
            if form.is_valid():
                organisation_name = form.cleaned_data['organisation_name']
                organisation_email = form.cleaned_data['organisation_email']
                organisation_website = form.cleaned_data['organisation_website']
                duplicate_results = organisation.objects.filter(Q(organisation_name=organisation_name) | Q(organisation_email=organisation_email) | Q(organisation_website=organisation_website))
                if duplicate_results.count() == 0 or request.POST.get('save_duplicate'):
                    submit_form = organisation(organisation_name=organisation_name,
                      organisation_email=organisation_email,
                      organisation_website=organisation_website,
                      change_user=(request.user))
                    submit_form.save()
                    return HttpResponseRedirect(reverse(organisation_information, args={submit_form.organisation_id}))
    else:
        form_errors = form.errors
    t = loader.get_template('NearBeach/new_organisation.html')
    duplication_count = 0
    if not duplicate_results == None:
        duplication_count = duplicate_results.count()
    c = {'new_organisation_form':form, 
     'duplicate_results':duplicate_results, 
     'duplication_count':duplication_count, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'form_errors':form_errors}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_permission_set(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_set')
    if permission_results['administration_create_permission_set'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    else:
        save_errors = None
        if request.method == 'POST' and permission_results['administration_create_permission_set'] >= 3:
            form = permission_set_form(request.POST)
            if form.is_valid():
                permission_set_name = form.cleaned_data['permission_set_name']
                permission_set_results = permission_set.objects.filter(is_deleted='FALSE',
                  permission_set_name=permission_set_name)
                if permission_set_results:
                    return HttpResponseRedirect(reverse('permission_set_information', args={permission_set_results[0].permission_set_id}))
                submit_permission_set = permission_set(permission_set_name=(form.cleaned_data['permission_set_name']),
                  administration_assign_user_to_group=(form.cleaned_data['administration_assign_user_to_group']),
                  administration_create_group=(form.cleaned_data['administration_create_group']),
                  administration_create_permission_set=(form.cleaned_data['administration_create_permission_set']),
                  administration_create_user=(form.cleaned_data['administration_create_user']),
                  assign_campus_to_customer=(form.cleaned_data['assign_campus_to_customer']),
                  associate_project_and_task=(form.cleaned_data['associate_project_and_task']),
                  bug=(form.cleaned_data['bug']),
                  bug_client=(form.cleaned_data['bug_client']),
                  customer=(form.cleaned_data['customer']),
                  email=(form.cleaned_data['email']),
                  invoice=(form.cleaned_data['invoice']),
                  invoice_product=(form.cleaned_data['invoice_product']),
                  kanban=(form.cleaned_data['kanban']),
                  kanban_card=(form.cleaned_data['kanban_card']),
                  opportunity=(form.cleaned_data['opportunity']),
                  organisation=(form.cleaned_data['organisation']),
                  organisation_campus=(form.cleaned_data['organisation_campus']),
                  project=(form.cleaned_data['project']),
                  quote=(form.cleaned_data['quote']),
                  request_for_change=(form.cleaned_data['request_for_change']),
                  requirement=(form.cleaned_data['requirement']),
                  requirement_link=(form.cleaned_data['requirement_link']),
                  tag=(form.cleaned_data['tag']),
                  task=(form.cleaned_data['task']),
                  tax=(form.cleaned_data['tax']),
                  template=(form.cleaned_data['template']),
                  whiteboard=(form.cleaned_data['whiteboard']),
                  document=(form.cleaned_data['document']),
                  contact_history=(form.cleaned_data['contact_history']),
                  kanban_comment=(form.cleaned_data['kanban_comment']),
                  project_history=(form.cleaned_data['project_history']),
                  task_history=(form.cleaned_data['task_history']),
                  change_user=(request.user))
                submit_permission_set.save()
                return HttpResponseRedirect(reverse('permission_set_information', args={submit_permission_set.permission_set_id}))
            print(form.errors)
            save_errors = form.errors
    t = loader.get_template('NearBeach/new_permission_set.html')
    c = {'permission_set_form':permission_set_form(request.POST or None), 
     'save_errors':save_errors, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_project(request, location_id='', destination=''):
    permission_results = return_user_permission_level(request, None, 'project')
    if permission_results['project'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    elif request.method == 'POST':
        form = new_project_form(request.POST)
        if form.is_valid():
            nearbeach_option_results = nearbeach_option.objects.latest('date_created')
            project_name = form.cleaned_data['project_name']
            project_description = form.cleaned_data['project_description']
            organisation_id_form = form.cleaned_data['organisation_id']
            project_story_point = form.cleaned_data['project_story_point']
            submit_project = project(project_name=project_name,
              project_description=project_description,
              project_start_date=(form.cleaned_data['project_start_date']),
              project_end_date=(form.cleaned_data['project_end_date']),
              project_status='Backlog',
              project_story_point_min=(project_story_point * nearbeach_option_results.story_point_hour_min),
              project_story_point_max=(project_story_point * nearbeach_option_results.story_point_hour_max),
              change_user=(request.user))
            if organisation_id_form:
                submit_project.organisation_id = organisation_id_form
            submit_project.save()
            project_permission = form.cleaned_data['project_permission']
            for row in project_permission:
                submit_group = object_assignment(project_id=submit_project,
                  group_id=group.objects.get(group_id=(row.group_id)),
                  change_user=(request.user))
                submit_group.save()

            if destination == 'customer':
                customer_instance = customer.objects.get(customer_id=location_id)
                save_project_customer = project_customer(project_id=submit_project,
                  customer_id=customer_instance,
                  change_user=(request.user))
                save_project_customer.save()
            else:
                if destination == 'opportunity':
                    opportunity_instance = opportunity.objects.get(opportunity_id=location_id)
                    object_assignment_save = object_assignment(project_id=submit_project,
                      opportunity_id=opportunity_instance,
                      change_user=(request.user))
                    object_assignment_save.save()
                else:
                    if destination == 'requirement':
                        requirement_instance = requirement.objects.get(requirement_id=location_id)
                        project_requirement_save = object_assignment(project_id=submit_project,
                          requirement_id=requirement_instance,
                          change_user=(request.user))
                        project_requirement_save.save()
                    else:
                        if destination == 'requirement_item':
                            requirement_item_instance = requirement_item.objects.get(requirement_item_id=location_id)
                            project_requirement_item_save = object_assignment(project_id=submit_project,
                              requirement_item_id=requirement_item_instance,
                              change_user=(request.user))
                            project_requirement_item_save.save()
                        if destination == 'organisation':
                            return HttpResponseRedirect(reverse(organisation_information, args={location_id}))
                        if destination == 'customer':
                            return HttpResponseRedirect(reverse(customer_information, args={location_id}))
                        if destination == 'opportunity':
                            return HttpResponseRedirect(reverse(opportunity_information, args={location_id}))
                        if destination == 'requirement':
                            return HttpResponseRedirect(reverse('requirement_information', args={location_id}))
                        if destination == 'requirement_item':
                            return HttpResponseRedirect(reverse('requirement_item_information', args={location_id}))
                        return HttpResponseRedirect(reverse(project_information, args={submit_project.pk}))
        else:
            print('Form is not valid')
            print(form.errors)
    current_user = request.user
    groups_results = group.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username_id=(current_user.id)).values('group_id')))
    organisations_results = organisation.objects.filter(is_deleted='FALSE')
    if destination == '' or destination == None:
        organisation_id = None
        customer_id = None
        opportunity_id = None
    else:
        if destination == 'organisation':
            organisation_id = location_id
            customer_id = None
            opportunity_id = None
        else:
            if destination == 'customer':
                organisation_id = customer.organisation_id
                customer_id = customer.customer_id
                opportunity_id = None
            else:
                if destination == 'opportunity':
                    opportunity_instance = opportunity.objects.get(opportunity_id=location_id)
                    organisation_id = None
                    customer_id = None
                    opportunity_id = opportunity_instance.opportunity_id
                else:
                    if destination == 'requirement':
                        requirement_instance = requirement.objects.get(requirement_id=location_id)
                        customer_id = None
                        organisation_id = requirement_instance.organisation_id
                        opportunity_id = None
                    else:
                        if destination == 'requirement_item':
                            requirement_item_instance = requirement_item.objects.get(requirement_item_id=location_id)
                            requirement_instance = requirement.objects.get(requirement_id=(requirement_item_instance.requirement_id.requirement_id))
                            customer_id = None
                            organisation_id = requirement_instance.organisation_id
                            opportunity_id = None
                        t = loader.get_template('NearBeach/new_project.html')
                        print(request.user.id)
                        c = {'new_project_form':new_project_form(initial={'organisation_id': organisation_id}), 
                         'groups_results':groups_results, 
                         'groups_count':groups_results.__len__(), 
                         'opportunity_id':opportunity_id, 
                         'organisations_count':organisations_results.count(), 
                         'organisation_id':organisation_id, 
                         'customer_id':customer_id, 
                         'timezone':settings.TIME_ZONE, 
                         'new_item_permission':permission_results['new_item'], 
                         'administration_permission':permission_results['administration'], 
                         'destination':destination, 
                         'location_id':location_id, 
                         'nearbeach_option':nearbeach_option}
                        return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_quote(request, destination, primary_key):
    permission_results = return_user_permission_level(request, None, 'quote')
    if permission_results['quote'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = new_quote_form(request.POST)
        if form.is_valid():
            quote_title = form.cleaned_data['quote_title']
            quote_terms = form.cleaned_data['quote_terms']
            quote_stage_id = form.cleaned_data['quote_stage_id']
            customer_notes = form.cleaned_data['customer_notes']
            select_groups = form.cleaned_data['select_groups']
            quote_valid_till = form.cleaned_data['quote_valid_till']
            quote_stage_instance = list_of_quote_stage.objects.get(quote_stage_id=(quote_stage_id.quote_stage_id))
            submit_quotes = quote(quote_title=quote_title,
              quote_terms=quote_terms,
              quote_stage_id=quote_stage_instance,
              customer_notes=customer_notes,
              quote_valid_till=quote_valid_till,
              change_user=(request.user))
            submit_quotes.quote_approval_status_id = 'APPROVED'
            if destination == 'project':
                submit_quotes.project_id = project.objects.get(project_id=primary_key)
            else:
                if destination == 'task':
                    submit_quotes.task_id = task.objects.get(task_id=primary_key)
                else:
                    if destination == 'customer':
                        submit_quotes.customer_id = customer.objects.get(customer_id=primary_key)
                    else:
                        if destination == 'organisation':
                            submit_quotes.organisation_id = organisation.objects.get(organisation_id=primary_key)
                        else:
                            submit_quotes.opportunity_id = opportunity.objects.get(opportunity_id=primary_key)
            submit_quotes.save()
            if select_groups:
                for row in select_groups:
                    group_instance = group.objects.get(group_name=row)
                    permission_save = object_assignment(quote_id=submit_quotes,
                      group_id=group_instance,
                      change_user=(request.user))
                    permission_save.save()

            if destination == 'customer':
                responsible_customer_submit = quote_responsible_customer(customer_id=customer.objects.get(customer_id=primary_key),
                  change_user=(request.user),
                  quote_id=submit_quotes)
                responsible_customer_submit.save()
            return HttpResponseRedirect(reverse(quote_information, args={submit_quotes.quote_id}))
        print(form.errors)
    end_date = datetime.datetime.now() + timedelta(14)
    t = loader.get_template('NearBeach/new_quote.html')
    c = {'new_quote_form':new_quote_form, 
     'primary_key':primary_key, 
     'destination':destination, 
     'end_year':end_date.year, 
     'end_month':end_date.month, 
     'end_day':end_date.day, 
     'timezone':settings.TIME_ZONE, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_quote_link(request, quote_id, destination, location_id=''):
    """

    :param request:
    :param quote_id: This is the quote we are going to link to
    :param destination: This is either a customer or organisation. That is the destination of what we want to link to
    :param location_id: only used in POST. This is the id of either the customer or organisation we are linking the quote to
    :return: A search list

    Method
    ~~~~~~
    1. Check if user has permission - send them to the naughty corner if they do not... those naughty people
    2. Check to see if the method is POST - obey the method in POST section from now on
    3. Check to see if the destination is either a customer or organisation. Get the appropriate data
        Note - limit the results to only those customers/organisations linked with the opportunity
    4. Get templates and context
    5. Render
    """
    permission_results = return_user_permission_level(request, None, 'quote')
    if permission_results['quote'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))
    elif request.method == 'POST':
        quote_update = quote.objects.get(quote_id=quote_id)
        if destination == 'organisation':
            quote_update.organisation_id = organisation.objects.get(organisation_id=location_id)
        else:
            quote_update.customer_id = customer.objects.get(customer_id=location_id)
        quote_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
        quote_results = quote.objects.get(quote_id=quote_id)
        opportunity_results = get_object_or_404(opportunity, opportunity_id=(quote_results.opportunity_id.opportunity_id))
        organisation_results = organisation.objects.filter(is_deleted='FALSE',
          organisation_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
          organisation_id__isnull=False,
          opportunity_id=(opportunity_results.opportunity_id)).values('organisation_id')))
        if destination == 'organisation':
            link_results = organisation_results
    else:
        link_results = customer.objects.filter(Q(is_deleted='FALSE') and Q(Q(customer_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
          customer_id__isnull=False,
          opportunity_id=(opportunity_results.opportunity_id)).values('customer_id'))) or Q(organisation_id__in=(organisation_results.values('organisation_id')))))
    t = loader.get_template('NearBeach/quote_information/new_quote_link.html')
    c = {'link_results':link_results, 
     'quote_results':quote_results, 
     'destination':destination, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_quote_template(request):
    permission_results = return_user_permission_level(request, None, 'templates')
    if permission_results['templates'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        quote_template_submit = quote_template(change_user_id=(request.user.id),
          quote_template_description='Quote Template',
          template_css='\n            .table_header {\n                font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;\n                border-collapse: collapse;\n                width: 100%;\n            }\n            \n            .table_header {\n                border: 1px solid #ddd;\n                padding: 8px;\n            }\n            \n            .table_header {\n                padding-top: 12px;\n                padding-bottom: 12px;\n                text-align: left;\n                background-color: #4CAF50;\n                color: white;\n            }\n            \n            table td, table td * {\n                vertical-align: top;\n            }\n            ',
          header='NearBeach Quote Number {{ quote_id }}',
          company_letter_head='<p>NearBeach Incorporated<br />Melbourne 3000<br />Australia</p>',
          payment_terms='Please pay within 30 days',
          notes='{{ quote_terms }}',
          organisation_details='\n                <p>{{ organisation_name }}<br />\n                {{ billing_address1 }}<br />\n                {{ billing_address2 }}<br />\n                {{ billing_address3 }}<br />\n                {{ billing_suburb }} {{ billing_postcode }}<br />\n                {{ billing_region }}<br />\n                {{ billing_country }}</p>\n            ',
          product_line='Temp product line',
          service_line='Temp service line',
          payment_method='\n            <table>\n            <tbody>\n            <tr style="height: 18px;">\n            <td style="width: 50%; height: 18px;">Account</td>\n            <td style="width: 50%; height: 18px;">0000 0000</td>\n            </tr>\n            <tr style="height: 18px;">\n            <td style="width: 50%; height: 18px;">BSB</td>\n            <td style="width: 50%; height: 18px;">000 000</td>\n            </tr>\n            <tr style="height: 18px;">\n            <td style="width: 50%; height: 18px;">Acount Name</td>\n            <td style="width: 50%; height: 18px;">NearBeach Holdings</td>\n            </tr>\n            </tbody>\n            </table>\n            ',
          footer='{{ page_number }}')
        quote_template_submit.save()
        json_data = {}
        json_data['quote_template_id'] = quote_template_submit.pk
        return JsonResponse(json_data)
    return HttpResponseBadRequest('Sorry, but new template can only be requested by a post command')


@login_required(login_url='login', redirect_field_name='')
def new_request_for_change(request):
    """
    A user would like to implement a new request for change. This new function will ask the user for the following set of
    information;
    - Basic Request for information
    - Basic risk, plan and implementation
    - Assigned groups
    :param request:
    :return: The new request for change page

    Method
    ~~~~~~
    1. Check user permission - if they can't do this then send them to the naughty corner
    2. Check to see if it is post - read notes in that section
    3. Gather the required fields
    4. Render the page
    """
    permission_results = return_user_permission_level(request, None, 'request_for_change')
    if permission_results['request_for_change'] <= 2:
        return HttpResponseRedirect(reverse('permission_denied'))
    form_errors = ''
    if request.method == 'POST':
        form = new_request_for_change_form(request.POST)
        if form.is_valid():
            rfc_submit = request_for_change(rfc_title=(form.cleaned_data['rfc_title']),
              rfc_type=(form.cleaned_data['rfc_type']),
              rfc_implementation_start_date=(form.cleaned_data['rfc_implementation_start_date']),
              rfc_implementation_end_date=(form.cleaned_data['rfc_implementation_end_date']),
              rfc_implementation_release_date=(form.cleaned_data['rfc_implementation_release_date']),
              rfc_version_number=(form.cleaned_data['rfc_version_number']),
              rfc_summary=(form.cleaned_data['rfc_summary']),
              rfc_lead=(form.cleaned_data['rfc_lead']),
              rfc_priority=(form.cleaned_data['rfc_priority']),
              rfc_risk=(form.cleaned_data['rfc_risk']),
              rfc_impact=(form.cleaned_data['rfc_impact']),
              rfc_risk_and_impact_analysis=(form.cleaned_data['rfc_risk_and_impact_analysis']),
              rfc_implementation_plan=(form.cleaned_data['rfc_implementation_plan']),
              rfc_backout_plan=(form.cleaned_data['rfc_backout_plan']),
              rfc_test_plan=(form.cleaned_data['rfc_test_plan']),
              change_user=(request.user),
              rfc_status=1)
            rfc_submit.save()
            rfc_permission = form.cleaned_data['rfc_permission']
            for row in rfc_permission:
                submit_group = object_assignment(request_for_change=rfc_submit,
                  group_id=group.objects.get(group_id=(row.group_id)),
                  change_user=(request.user))
                submit_group.save()

            return HttpResponseRedirect(reverse('request_for_change_draft', args={rfc_submit.rfc_id}))
        print(form.errors)
        form_errors = form.errors
    t = loader.get_template('NearBeach/new_request_for_change.html')
    c = {'new_request_for_change_form':new_request_for_change_form(), 
     'form_errors':form_errors, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_task(request, location_id='', destination=''):
    permission_results = return_user_permission_level(request, None, 'task')
    if permission_results['task'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        form = new_task_form(request.POST)
        if form.is_valid():
            nb_results = nearbeach_option.objects.latest('date_created')
            task_story_point_min = form.cleaned_data['task_story_point'] * nb_results.story_point_hour_min
            task_story_point_max = form.cleaned_data['task_story_point'] * nb_results.story_point_hour_max
            task_short_description = form.cleaned_data['task_short_description']
            task_long_description = form.cleaned_data['task_long_description']
            organisation_id_form = form.cleaned_data['organisation_id']
            submit_task = task(task_short_description=task_short_description,
              task_long_description=task_long_description,
              task_start_date=(form.cleaned_data['task_start_date']),
              task_end_date=(form.cleaned_data['task_end_date']),
              task_status='Backlog',
              change_user=(request.user),
              task_story_point_min=task_story_point_min,
              task_story_point_max=task_story_point_max)
            if organisation_id_form:
                submit_task.organisation_id = organisation_id_form
            submit_task.save()
            task_permission = form.cleaned_data['task_permission']
            for row in task_permission:
                submit_group = object_assignment(task_id_id=(submit_task.pk),
                  group_id_id=(row.group_id),
                  change_user=(request.user))
                submit_group.save()

            if destination == 'customer':
                customer_instance = customer.objects.get(customer_id=location_id)
                save_project_customer = task_customer(task_id=submit_task,
                  customer_id=customer_instance,
                  change_user=(request.user))
                save_project_customer.save()
            else:
                if destination == 'opportunity':
                    opportunity_instance = opportunity.objects.get(opportunity_id=location_id)
                    object_assignment_submit = object_assignment(task_id=submit_task,
                      opportunity_id=opportunity_instance,
                      change_user=(request.user))
                    object_assignment_submit.save()
                else:
                    if destination == 'requirement':
                        requirement_instance = requirement.objects.get(requirement_id=location_id)
                        object_assignment_submit = object_assignment(task_id=submit_task,
                          requirement_id=requirement_instance,
                          change_user=(request.user))
                        object_assignment_submit.save()
                    else:
                        if destination == 'requirement_item':
                            requirement_item_instance = requirement_item.objects.get(requirement_item_id=location_id)
                            object_assignment_submit = object_assignment(task_id=submit_task,
                              requirement_item_id=requirement_item_instance,
                              change_user=(request.user))
                            object_assignment_submit.save()
                        else:
                            if destination == 'project':
                                project_instance = project.objects.get(project_id=location_id)
                                object_assignment_submit = object_assignment(task_id=submit_task,
                                  project_id=project_instance,
                                  change_user=(request.user))
                                object_assignment_submit.save()
                            if destination == 'organisation':
                                return HttpResponseRedirect(reverse(organisation_information, args={location_id}))
                            if destination == 'customer':
                                return HttpResponseRedirect(reverse(customer_information, args={location_id}))
                            if destination == 'opportunity':
                                return HttpResponseRedirect(reverse(opportunity_information, args={location_id}))
                            if destination == 'requirement':
                                return HttpResponseRedirect(reverse('requirement_information', args={location_id}))
                            if destination == 'requirement_item':
                                return HttpResponseRedirect(reverse('requirement_item_information', args={location_id}))
                            if destination == 'project':
                                return HttpResponseRedirect(reverse('project_information', args={location_id}))
                            return HttpResponseRedirect(reverse(task_information, args={submit_task.pk}))
        else:
            groups_results = group.objects.filter(is_deleted='FALSE',
              group_id__in=(user_group.objects.filter(is_deleted='FALSE',
              username_id=(request.user.id)).values('group_id')))
            organisations_results = organisation.objects.filter(is_deleted='FALSE')
            today = datetime.datetime.now()
            next_week = today + datetime.timedelta(days=31)
            if destination == '' or destination == None:
                organisation_id = None
                customer_id = None
                opportunity_id = None
    elif destination == 'organisation':
        organisation_id = location_id
        customer_id = None
        opportunity_id = None
    else:
        if destination == 'customer':
            customer_instance = customer.objects.get(customer_id=location_id)
            organisation_id = customer.organisation_id
            customer_id = customer.customer_id
            opportunity_id = None
        else:
            if destination == 'project':
                project_instance = project.objects.get(project_id=location_id)
                organisation_id = project_instance.organisation_id
                customer_id = project_instance.customer_id
                opportunity_id = None
            else:
                if destination == 'opportunity':
                    opportunity_instance = opportunity.objects.get(opportunity_id=location_id)
                    organisation_id = None
                    customer_id = None
                    opportunity_id = opportunity_instance.opportunity_id
                else:
                    if destination == 'requirement':
                        requirement_instance = requirement.objects.get(requirement_id=location_id)
                        organisation_id = requirement_instance.organisation_id
                        customer_id = None
                        opportunity_id = None
                    else:
                        if destination == 'requirement_item':
                            requirement_instance = requirement.objects.get(requirement_id__in=(requirement_item.objects.filter(requirement_item_id=location_id).values('requirement_id')))
                            organisation_id = requirement_instance.organisation_id
                            customer_id = None
                            opportunity_id = None
                        t = loader.get_template('NearBeach/new_task.html')
                        c = {'new_task_form':new_task_form(initial={'organisation_id': organisation_id}), 
                         'groups_results':groups_results, 
                         'groups_count':groups_results.__len__(), 
                         'organisation_id':organisation_id, 
                         'organisations_count':organisation.objects.filter(is_deleted='FALSE').count(), 
                         'nearbeach_option':nearbeach_option.objects.latest('date_created'), 
                         'customer_id':customer_id, 
                         'opportunity_id':opportunity_id, 
                         'timezone':settings.TIME_ZONE, 
                         'location_id':location_id, 
                         'destination':destination, 
                         'new_item_permission':permission_results['new_item'], 
                         'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_whiteboard(request, location_id, destination, folder_id):
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'whiteboard')
        if permission_results['whiteboard'] <= 2:
            return HttpResponseRedirect(reverse('permission_denied'))
        form = new_whiteboard_form(request.POST)
        if form.is_valid():
            whiteboard_submit = whiteboard(whiteboard_title=(form.cleaned_data['whiteboard_name']),
              whiteboard_xml=('\n                    <mxGraphModel><root>\n                        <Workflow label="%s" description="" href="" id="0"><mxCell/></Workflow>\n                        <Layer label="Default Layer" id="1"><mxCell parent="0"/></Layer>\n                    </root></mxGraphModel>\n                ' % form.cleaned_data['whiteboard_name']),
              change_user=(request.user))
            whiteboard_submit.save()
            document_submit = document(document_description=(form.cleaned_data['whiteboard_name']),
              whiteboard=whiteboard_submit,
              change_user=(request.user))
            document_submit.save()
            document_permission_submit = document_permission(document_key=document_submit,
              change_user=(request.user))
            if destination == 'project':
                document_permission_submit.project_id = project.objects.get(project_id=location_id)
            else:
                if destination == 'task':
                    document_permission_submit.task_id = task.objects.get(task_id=location_id)
                else:
                    if destination == 'requirement':
                        document_permission_submit.requirement_id = requirement.objects.get(requirement_id=location_id)
                    else:
                        if destination == 'requirement_item':
                            document_permission_submit.requirement_item_id = requirement_item.objects.get(requirement_item_id=location_id)
                        else:
                            if destination == 'opportunity':
                                document_permission_submit.opportunity_id = opportunity.objects.get(opportunity_id=location_id)
                            else:
                                if destination == 'customer':
                                    document_permission_submit.customer_id = customer.objects.get(customer_id=location_id)
                                else:
                                    if destination == 'organisation':
                                        document_permission_submit.organisation_id = organisation.objects.get(organisation_id=location_id)
                                    document_permission_submit.save()
                                    t = loader.get_template('NearBeach/blank.html')
                                    c = {}
                                    return HttpResponse(t.render(c, request))
        print(form.errors)
    else:
        return HttpResponseBadRequest('Sorry, this has to be through post')


@login_required(login_url='login', redirect_field_name='')
def opportunity_delete_permission(request, opportunity_permissions_id):
    if request.method == 'POST':
        opportunity_permission_update = opportunity_permission.objects.get(opportunity_permissions_id=opportunity_permissions_id)
        opportunity_permission_update.is_deleted = 'TRUE'
        opportunity_permission_update.change_user = request.user
        opportunity_permission_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this has to be through post')


@login_required(login_url='login', redirect_field_name='')
def opportunity_connection_list(request, opportunity_id):
    permission_results = return_user_permission_level(request, None, 'opportunity')
    if permission_results['opportunity'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    customer_connection_results = customer.objects.filter(is_deleted='FALSE',
      customer_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id,
      customer_id__isnull=False).values('customer_id'))).order_by('customer_first_name', 'customer_last_name')
    organisation_connection_results = organisation.objects.filter(is_deleted='FALSE',
      organisation_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id,
      organisation_id__isnull=False).values('organisation_id')))
    opportunity_results = opportunity.objects.get(opportunity_id=opportunity_id)
    t = loader.get_template('NearBeach/opportunity_information/opportunity_connection_list.html')
    c = {'customer_connection_results':customer_connection_results, 
     'organisation_connection_results':organisation_connection_results, 
     'opportunity_results':opportunity_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'opportunity_permission':permission_results['opportunity']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def opportunity_information(request, opportunity_id):
    permission_results = return_user_permission_level(request, None, 'opportunity')
    if permission_results['opportunity'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    if permission_results['opportunity'] == 1:
        return HttpResponseRedirect(reverse('opportunity_readonly', args={opportunity_id}))
    opportunity_results = opportunity.objects.get(opportunity_id=opportunity_id)
    if opportunity_results.opportunity_stage_id.opportunity_closed == 'TRUE':
        return HttpResponseRedirect(reverse('opportunity_readonly', args={opportunity_id}))
        object_access = object_assignment.objects.filter(is_deleted='FALSE',
          opportunity_id=opportunity_id,
          group_id__in=(user_group.objects.filter(is_deleted='FALSE',
          username=(request.user)).values('group_id')))
        if object_access.count() == 0:
            if not permission_results['administration'] == 4:
                return HttpResponseRedirect(reverse('permission_denied'))
        if request.method == 'POST':
            form = opportunity_information_form(request.POST, request.FILES)
            if form.is_valid():
                current_user = request.user
                save_opportunity = opportunity.objects.get(opportunity_id=opportunity_id)
                save_opportunity.opportunity_name = form.cleaned_data['opportunity_name']
                save_opportunity.opportunity_description = form.cleaned_data['opportunity_description']
                save_opportunity.opportunity_amount = form.cleaned_data['opportunity_amount']
                save_opportunity.opportunity_success_probability = form.cleaned_data['opportunity_success_probability']
                save_opportunity.opportunity_expected_close_date = form.cleaned_data['opportunity_expected_close_date']
                save_opportunity.change_user = request.user
                save_opportunity.currency_id = list_of_currency.objects.get(currency_id=(int(request.POST['currency_id'])))
                save_opportunity.amount_type_id = list_of_amount_type.objects.get(amount_type_id=(int(request.POST['amount_type_id'])))
                save_opportunity.opportunity_stage_id = list_of_opportunity_stage.objects.get(opportunity_stage_id=(int(request.POST['opportunity_stage_id'])))
                save_opportunity.save()
                opportunity_instance = opportunity.objects.get(opportunity_id=opportunity_id)
                next_step = form.cleaned_data['next_step']
                if not next_step == '':
                    save_next_step = opportunity_next_step(opportunity_id=opportunity_instance,
                      next_step_description=next_step,
                      change_user_id=(request.user.id),
                      user_id=current_user)
                    save_next_step.save()
                select_groups = form.cleaned_data['select_groups']
                if select_groups:
                    for row in select_groups:
                        group_instance = group.objects.get(group_id=(row.group_id))
                        permission_save = object_access(opportunity_id=opportunity_instance,
                          group_id=group_instance,
                          user_id=current_user,
                          change_user=(request.user))
                        permission_save.save()

                    object_access.objects.filter(opportunity_id=opportunity_id,
                      all_user='TRUE',
                      is_deleted='FALSE').update(is_deleted='TRUE')
                select_users = form.cleaned_data['select_users']
                print(select_users)
                if select_users:
                    for row in select_users:
                        assigned_user_instance = auth.models.User.objects.get(username=row)
                        permission_save = object_access(opportunity_id=opportunity_instance,
                          assigned_user=assigned_user_instance,
                          user_id=current_user,
                          change_user=(request.user))
                        permission_save.save()

                    object_access.objects.filter(opportunity_id=opportunity_id,
                      all_user='TRUE',
                      is_deleted='FALSE').update(is_deleted='TRUE')
        else:
            print(form.errors)
    else:
        user_groups_results = user_group.objects.filter(username=(request.user))
        opportunity_permission_results = object_assignment.objects.filter(Q(Q(assigned_user=(request.user)) | Q(group_id__in=(user_groups_results.values('group_id')))) & Q(opportunity_id=opportunity_id))
        if not opportunity_permission_results:
            return HttpResponseRedirect(reverse(permission_denied))
        requirement_results = requirement.objects.filter(is_deleted='FALSE',
          requirement_id__in=(object_assignment.objects.filter(opportunity_id=opportunity_id,
          requirement_id__isnull=False).values('requirement_id')))
        project_results = project.objects.filter(is_deleted='FALSE',
          project_id__in=(object_assignment.objects.filter(opportunity_id=opportunity_id,
          project_id__isnull=False,
          is_deleted='FALSE').values('project_id')))
        task_results = task.objects.filter(is_deleted='FALSE',
          task_id__in=(object_assignment.objects.filter(opportunity_id=opportunity_id,
          task_id__isnull=False,
          is_deleted='FALSE').values('task_id')))
        group_permissions = object_assignment.objects.filter(group_id__isnull=False,
          opportunity_id=opportunity_id,
          is_deleted='FALSE').distinct()
        user_permissions = auth.models.User.objects.filter(id__in=(object_assignment.objects.filter(assigned_user__isnull=False,
          opportunity_id=opportunity_id,
          is_deleted='FALSE').values('assigned_user').distinct()))
        quote_results = quote.objects.filter(is_deleted='FALSE',
          opportunity_id=opportunity_id)
        t = loader.get_template('NearBeach/opportunity_information.html')
        c = {'opportunity_id':str(opportunity_id), 
         'opportunity_information_form':opportunity_information_form(instance=opportunity_results), 
         'opportunity_results':opportunity_results, 
         'group_permission':group_permissions, 
         'user_permissions':user_permissions, 
         'project_results':project_results, 
         'task_results':task_results, 
         'quote_results':quote_results, 
         'requirement_results':requirement_results, 
         'opportunity_perm':permission_results['opportunity'], 
         'timezone':settings.TIME_ZONE, 
         'new_item_permission':permission_results['new_item'], 
         'administration_permission':permission_results['administration'], 
         'opportunity_permission':permission_results['opportunity'], 
         'opportunity_close_form':opportunity_close_form()}
        return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def opportunity_readonly(request, opportunity_id):
    """
    The read only module for the user
    :param request:
    :param opportunity_id:
    :return:
    Method
    ~~~~~~
    1. Get group information of the user
    2. Check user permissions - send them to the naughty place if they do not have any
    3. Get all relivant data for the read only template
    4. Get the read only template
    5. Render results
    """
    group_results = group.objects.filter(is_deleted='FALSE',
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username_id=(request.user),
      group_id__isnull=False).values('group_id')))
    permission_results = return_user_permission_level(request, group_results.values('group_id'), 'opportunity')
    if permission_results['opportunity'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    opportunity_results = opportunity.objects.get(opportunity_id=opportunity_id)
    customer_connection_results = customer.objects.filter(is_deleted='FALSE',
      customer_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id,
      customer_id__isnull=False).values('customer_id'))).order_by('customer_first_name', 'customer_last_name')
    organisation_connection_results = organisation.objects.filter(is_deleted='FALSE',
      organisation_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id,
      organisation_id__isnull=False).values('organisation_id')))
    to_do_results = to_do.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id)
    email_results = email_content.objects.filter(is_deleted='FALSE',
      email_content_id__in=(email_contact.objects.filter(Q(opportunity_id=opportunity_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
    requirement_results = requirement.objects.filter(is_deleted='FALSE',
      requirement_id__in=(object_assignment.objects.filter(opportunity_id=opportunity_id,
      requirement_id__isnull=False).values('requirement_id')))
    project_results = project.objects.filter(is_deleted='FALSE',
      project_id__in=(object_assignment.objects.filter(opportunity_id=opportunity_id,
      project_id__isnull=False,
      is_deleted='FALSE').values('project_id')))
    task_results = task.objects.filter(is_deleted='FALSE',
      task_id__in=(object_assignment.objects.filter(opportunity_id=opportunity_id,
      task_id__isnull=False,
      is_deleted='FALSE').values('task_id')))
    tag_results = tag.objects.filter(is_deleted='FALSE',
      tag_id__in=(tag_assignment.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id).values('tag_id')))
    quote_results = quote.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id)
    group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id).exclude(group_id=None)
    assigned_user_results = object_assignment.objects.filter(is_deleted='FALSE',
      opportunity_id=opportunity_id).exclude(assigned_user=None)
    t = loader.get_template('NearBeach/opportunity_information/opportunity_readonly.html')
    c = {'opportunity_results':opportunity_results, 
     'opportunity_readonly_form':opportunity_readonly_form(initial={'opportunity_description': opportunity_results.opportunity_description}), 
     'timezone':datetime.timezone, 
     'customer_connection_results':customer_connection_results, 
     'organisation_connection_results':organisation_connection_results, 
     'to_do_results':to_do_results, 
     'email_results':email_results, 
     'requirement_results':requirement_results, 
     'project_results':project_results, 
     'task_results':task_results, 
     'tag_results':tag_results, 
     'quote_results':quote_results, 
     'group_list_results':group_list_results, 
     'assigned_user_results':assigned_user_results, 
     'opportunity_permission':permission_results['opportunity'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def organisation_information(request, organisation_id):
    permission_results = return_user_permission_level(request, None, ['organisation', 'organisation_campus', 'customer'])
    if permission_results['organisation'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    if permission_results['organisation'] == 1:
        return HttpResponseRedirect(reverse('organisation_readonly', args={organisation_id}))
    if request.method == 'POST':
        if permission_results['organisation'] > 1:
            form = organisation_information_form(request.POST, request.FILES)
            if form.is_valid():
                save_data = organisation.objects.get(organisation_id=organisation_id)
                save_data.organisation_name = form.cleaned_data['organisation_name']
                save_data.organisation_website = form.cleaned_data['organisation_website']
                save_data.organisation_email = form.cleaned_data['organisation_email']
                save_data.change_user = request.user
                update_profile_picture = request.FILES.get('update_profile_picture')
                if not update_profile_picture == None:
                    save_data.organisation_profile_picture = update_profile_picture
                save_data.save()
    organisation_results = get_object_or_404(organisation,
      organisation_id=organisation_id,
      is_deleted='FALSE')
    campus_results = campus.objects.filter(organisation_id=organisation_id,
      is_deleted='FALSE')
    customer_results = customer.objects.filter(organisation_id=organisation_results,
      is_deleted='FALSE')
    quote_results = quote.objects.filter(is_deleted='FALSE',
      organisation_id=organisation_id)
    project_results = project.objects.filter(organisation_id=organisation_id,
      is_deleted='FALSE')
    task_results = task.objects.filter(organisation_id=organisation_id,
      is_deleted='FALSE')
    user_groups_results = user_group.objects.filter(is_deleted='FALSE',
      username=(request.user))
    opportunity_permissions_results = object_assignment.objects.filter(Q(Q(assigned_user=(request.user)) | Q(group_id__in=(user_groups_results.values('group_id')))))
    opportunity_results = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      organisation_id=organisation_id,
      opportunity_id__in=(opportunity_permissions_results.values('opportunity_id'))).values('opportunity_id')))
    today = datetime.datetime.now()
    t = loader.get_template('NearBeach/organisation_information.html')
    try:
        profile_picture = organisation_results.organisation_profile_picture.url
    except:
        profile_picture = ''

    c = {'organisation_results':organisation_results, 
     'campus_results':campus_results, 
     'customer_results':customer_results, 
     'organisation_information_form':organisation_information_form(instance=organisation_results,
       initial={'start_date_year':today.year, 
      'start_date_month':today.month, 
      'start_date_day':today.day}), 
     'profile_picture':profile_picture, 
     'project_results':project_results, 
     'task_results':task_results, 
     'opportunity_results':opportunity_results, 
     'PRIVATE_MEDIA_URL':settings.PRIVATE_MEDIA_URL, 
     'organisation_id':organisation_id, 
     'organisation_permissions':permission_results['organisation'], 
     'organisation_campus_permissions':permission_results['organisation_campus'], 
     'customer_permissions':permission_results['customer'], 
     'quote_results':quote_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def organisation_readonly(request, organisation_id):
    permission_results = return_user_permission_level(request, None, [
     'organisation', 'organisation_campus', 'customer'])
    if permission_results['organisation'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    organisation_results = organisation.objects.get(pk=organisation_id)
    campus_results = campus.objects.filter(organisation_id=organisation_id,
      is_deleted='FALSE')
    customer_results = customer.objects.filter(organisation_id=organisation_results,
      is_deleted='FALSE')
    quote_results = quote.objects.filter(is_deleted='FALSE',
      organisation_id=organisation_id)
    project_results = project.objects.filter(organisation_id=organisation_id,
      is_deleted='FALSE')
    task_results = task.objects.filter(organisation_id=organisation_id,
      is_deleted='FALSE')
    user_group_results = user_group.objects.filter(is_deleted='FALSE',
      group_id__isnull=False,
      username=(request.user))
    opportunity_permissions_results = object_assignment.objects.filter(Q(Q(assigned_user=(request.user)) | Q(group_id__in=(user_group_results.values('group_id')))))
    opportunity_results = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_id__in=(object_assignment.objects.filter(organisation_id=organisation_id,
      opportunity_id__in=(opportunity_permissions_results.values('opportunity_id'))).values('opportunity_id')))
    contact_history_results = contact_history.objects.filter(is_deleted='FALSE',
      organisation_id=organisation_id)
    contact_history_collective = []
    for row in contact_history_results:
        contact_history_collective.append(contact_history_readonly_form(initial={'contact_history':row.contact_history, 
         'submit_history':row.user_id.username + ' - ' + row.date_created.strftime('%d %B %Y %H:%M.%S')},
          contact_history_id=(row.contact_history_id)))

    email_results = email_content.objects.filter(is_deleted='FALSE',
      email_content_id__in=(email_contact.objects.filter(Q(is_deleted='FALSE') & Q(organisation_id=organisation_id) & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
    today = datetime.datetime.now()
    t = loader.get_template('NearBeach/organisation_information/organisation_readonly.html')
    try:
        profile_picture = organisation_results.organisation_profile_picture.url
    except:
        profile_picture = ''

    c = {'organisation_results':organisation_results, 
     'campus_results':campus_results, 
     'customer_results':customer_results, 
     'organisation_readonly_form':organisation_readonly_form(instance=organisation_results), 
     'profile_picture':profile_picture, 
     'project_results':project_results, 
     'task_results':task_results, 
     'opportunity_results':opportunity_results, 
     'PRIVATE_MEDIA_URL':settings.PRIVATE_MEDIA_URL, 
     'organisation_id':organisation_id, 
     'organisation_permissions':permission_results['organisation'], 
     'organisation_campus_permissions':permission_results['organisation_campus'], 
     'customer_permissions':permission_results['customer'], 
     'quote_results':quote_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'contact_history_collective':contact_history_collective, 
     'email_results':email_results}
    return HttpResponse(t.render(c, request))


def pdf_example(request):
    t = loader.get_template('NearBeach/diagnostic/pdf_example.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def permission_denied(request):
    t = loader.get_template('NearBeach/permission_denied.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def permission_set_information(request, permission_set_id):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_set')
    if permission_results['administration_create_permission_set'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    if request.method == 'POST':
        if permission_results['administration_create_permission_set'] == 1:
            return HttpResponseRedirect(reverse('permission_denied'))
        form = permission_set_form(request.POST)
        if form.is_valid():
            permission_set_update = permission_set.objects.get(permission_set_id=permission_set_id)
            permission_set_update.permission_set_name = form.cleaned_data['permission_set_name']
            permission_set_update.administration_assign_user_to_group = form.cleaned_data['administration_assign_user_to_group']
            permission_set_update.administration_create_group = form.cleaned_data['administration_create_group']
            permission_set_update.administration_create_permission_set = form.cleaned_data['administration_create_permission_set']
            permission_set_update.administration_create_user = form.cleaned_data['administration_create_user']
            permission_set_update.assign_campus_to_customer = form.cleaned_data['assign_campus_to_customer']
            permission_set_update.associate_project_and_task = form.cleaned_data['associate_project_and_task']
            permission_set_update.bug = form.cleaned_data['bug']
            permission_set_update.bug_client = form.cleaned_data['bug_client']
            permission_set_update.customer = form.cleaned_data['customer']
            permission_set_update.email = form.cleaned_data['email']
            permission_set_update.invoice = form.cleaned_data['invoice']
            permission_set_update.invoice_product = form.cleaned_data['invoice_product']
            permission_set_update.kanban = form.cleaned_data['kanban']
            permission_set_update.kanban_card = form.cleaned_data['kanban_card']
            permission_set_update.opportunity = form.cleaned_data['opportunity']
            permission_set_update.organisation = form.cleaned_data['organisation']
            permission_set_update.organisation_campus = form.cleaned_data['organisation_campus']
            permission_set_update.project = form.cleaned_data['project']
            permission_set_update.quote = form.cleaned_data['quote']
            permission_set_update.request_for_change = form.cleaned_data['request_for_change']
            permission_set_update.requirement = form.cleaned_data['requirement']
            permission_set_update.requirement_link = form.cleaned_data['requirement_link']
            permission_set_update.tag = form.cleaned_data['tag']
            permission_set_update.task = form.cleaned_data['task']
            permission_set_update.tax = form.cleaned_data['tax']
            permission_set_update.template = form.cleaned_data['template']
            permission_set_update.whiteboard = form.cleaned_data['whiteboard']
            permission_set_update.document = form.cleaned_data['document']
            permission_set_update.contact_history = form.cleaned_data['contact_history']
            permission_set_update.kanban_comment = form.cleaned_data['kanban_comment']
            permission_set_update.project_history = form.cleaned_data['project_history']
            permission_set_update.task_history = form.cleaned_data['task_history']
            permission_set_update.change_user = request.user
            permission_set_update.save()
            return HttpResponseRedirect(reverse('search_permission_set'))
    permission_set_results = permission_set.objects.get(permission_set_id=permission_set_id)
    t = loader.get_template('NearBeach/permission_set_information.html')
    c = {'permission_set_form':permission_set_form(initial={'permission_set_name':permission_set_results.permission_set_name, 
      'administration_assign_user_to_group':permission_set_results.administration_assign_user_to_group, 
      'administration_create_group':permission_set_results.administration_create_group, 
      'administration_create_permission_set':permission_set_results.administration_create_permission_set, 
      'administration_create_user':permission_set_results.administration_create_user, 
      'assign_campus_to_customer':permission_set_results.assign_campus_to_customer, 
      'associate_project_and_task':permission_set_results.associate_project_and_task, 
      'bug':permission_set_results.bug, 
      'bug_client':permission_set_results.bug_client, 
      'customer':permission_set_results.customer, 
      'email':permission_set_results.email, 
      'invoice':permission_set_results.invoice, 
      'invoice_product':permission_set_results.invoice_product, 
      'kanban':permission_set_results.kanban, 
      'kanban_card':permission_set_results.kanban_card, 
      'opportunity':permission_set_results.opportunity, 
      'organisation':permission_set_results.organisation, 
      'organisation_campus':permission_set_results.organisation_campus, 
      'project':permission_set_results.project, 
      'quote':permission_set_results.quote, 
      'request_for_change':permission_set_results.request_for_change, 
      'requirement':permission_set_results.requirement, 
      'requirement_link':permission_set_results.requirement_link, 
      'tag':permission_set_results.tag, 
      'task':permission_set_results.task, 
      'tax':permission_set_results.tax, 
      'template':permission_set_results.template, 
      'whiteboard':permission_set_results.whiteboard, 
      'document':permission_set_results.document, 
      'contact_history':permission_set_results.contact_history, 
      'kanban_comment':permission_set_results.kanban_comment, 
      'project_history':permission_set_results.project_history, 
      'task_history':permission_set_results.task_history}), 
     'permission_set_id':permission_set_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def permission_set_remove(request, permission_set_id, group_id):
    """
    This will remove the permission set from the groups.
    :param request:
    :param permission_set_id: The permission set id we are removing
    :param group_id: The group we will be removing the permission set from
    :return: blank page

    Method
    ~~~~~~
    1. If permission_set_id == 1 AND group_id == 1, then fail... we do not want to delete the admin group
    2. Check to see if request method is POST
    3. Check to see if user has permission
    4. Apply changes
    5. Remove users who have this set permission too ;)
    6. Send back blank page
    """
    if permission_set_id == 1:
        if group_id == 1:
            return HttpResponseBadRequest('Can not delete the admin permission from the admin group!!!')
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'administration_create_group')
        if permission_results['administration_create_group'] < 4:
            return HttpResponseRedirect(reverse('permission_denied'))
        group_permission.objects.filter(is_deleted='FALSE',
          group_id=group_id,
          permission_set_id=permission_set_id).update(is_deleted='TRUE')
        user_group.objects.filter(is_deleted='FALSE',
          group_id=group_id,
          permission_set_id=permission_set_id).update(is_deleted='TRUE')
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - this can only be done in post')


def preview_quote(request, quote_uuid, quote_template_id):
    quote_results = quote.objects.get(quote_uuid=quote_uuid)
    quote_id = quote_results.quote_id
    product_results = quote_product_and_service.objects.filter(is_deleted='FALSE',
      product_and_service__in=(product_and_service.objects.filter(product_or_service='Product').values('pk')),
      quote_id=quote_id)
    service_results = quote_product_and_service.objects.filter(is_deleted='FALSE',
      product_and_service__in=(product_and_service.objects.filter(product_or_service='Service').values('pk')),
      quote_id=quote_id)
    quote_template_results = quote_template.objects.get(quote_template_id=quote_template_id)
    template_css = update_template_strings(quote_template_results.template_css, quote_results)
    header = update_template_strings(quote_template_results.header, quote_results)
    company_letter_head = update_template_strings(quote_template_results.company_letter_head, quote_results)
    payment_terms = update_template_strings(quote_template_results.payment_terms, quote_results)
    notes = update_template_strings(quote_template_results.notes, quote_results)
    organisation_details = update_template_strings(quote_template_results.organisation_details, quote_results)
    product_line = update_template_strings(quote_template_results.product_line, quote_results)
    service_line = update_template_strings(quote_template_results.service_line, quote_results)
    payment_method = update_template_strings(quote_template_results.payment_method, quote_results)
    footer = update_template_strings(quote_template_results.footer, quote_results)
    product_unadjusted_price = product_results.aggregate(Sum('product_price'))
    product_discount = product_results.aggregate(Sum('discount_amount'))
    product_sales_price = product_results.aggregate(Sum('sales_price'))
    product_tax = product_results.aggregate(Sum('tax'))
    product_total = product_results.aggregate(Sum('total'))
    service_unadjusted_price = service_results.aggregate(Sum('product_price'))
    service_discount = service_results.aggregate(Sum('discount_amount'))
    service_sales_price = service_results.aggregate(Sum('sales_price'))
    service_tax = service_results.aggregate(Sum('tax'))
    service_total = service_results.aggregate(Sum('total'))
    current_date = datetime.datetime.now()
    t = loader.get_template('NearBeach/render_templates/quote_template.html')
    c = {'template_css':template_css, 
     'header':header, 
     'company_letter_head':company_letter_head, 
     'payment_terms':payment_terms, 
     'notes':notes, 
     'organisation_details':organisation_details, 
     'product_line':product_line, 
     'service_line':service_line, 
     'payment_method':payment_method, 
     'footer':footer, 
     'product_unadjusted_price':product_unadjusted_price, 
     'product_discount':product_discount, 
     'product_sales_price':product_sales_price, 
     'product_tax':product_tax, 
     'product_total':product_total, 
     'service_unadjusted_price':service_unadjusted_price, 
     'service_discount':service_discount, 
     'service_sales_price':service_sales_price, 
     'service_tax':service_tax, 
     'service_total':service_total, 
     'current_user':request.user, 
     'quote_id':quote_id, 
     'current_date':current_date, 
     'quote_results':quote_results, 
     'product_results':product_results, 
     'service_results':service_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def preview_requirement(request, requirement_id):
    """
    This is a read only document output of the requirements. It will contain the following information;
    - Title page + requirement information
    - Requirement Scope
    - Requirement item table
    - Requirement item information
    - Apendix A: Requirement and Requirement Item Links

    :param request:
    :param requirement_id:
    :return: Read only form

    Method
    ~~~~~~
    1. Collect data
    2. Obtain templates
    3. Render templates
    4. Return HTML to user.
    """
    requirement_results = requirement.objects.get(requirement_id=requirement_id)
    requirement_link_results = requirement_link.objects.filter(is_deleted='FALSE',
      requirement_id=requirement_id)
    requirement_item_results = requirement_item.objects.filter(is_deleted='FALSE',
      requirement_id=requirement_id)
    requirement_item_link_results = requirement_item_link.objects.filter(is_deleted='FALSE',
      requirement_item_id__in=(requirement_item_results.values('requirement_item_id')))
    t = loader.get_template('NearBeach/requirement_information/preview_requirement.html')
    c = {'requirement_results':requirement_results, 
     'requirement_link_results':requirement_item_results, 
     'requirement_item_results':requirement_item_results, 
     'requirement_item_link_results':requirement_item_link_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def private_document(request, document_key):
    """
    This is temp code. Hopefully I will make this function
    a lot better
    """
    PRIVATE_MEDIA_ROOT = settings.PRIVATE_MEDIA_ROOT
    document_results = document.objects.get(pk=document_key)
    if document_results.document_url_location:
        return HttpResponseRedirect(document_results.document_url_location)
    path = PRIVATE_MEDIA_ROOT + '/' + document_results.document.name
    return server.serve(request, path=path)


@login_required(login_url='login', redirect_field_name='')
def project_information(request, project_id):
    project_groups_results = object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id).values('group_id')
    permission_results = return_user_permission_level(request, project_groups_results, ['project', 'project_history'])
    if permission_results['project'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    object_access = object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id,
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id')))
    if object_access.count() == 0:
        if not permission_results['administration'] == 4:
            return HttpResponseRedirect(reverse('permission_denied'))
    elif request.method == 'POST':
        if permission_results['project'] >= 2:
            form = project_information_form(request.POST, request.FILES)
            if form.is_valid():
                project_results = project.objects.get(project_id=project_id)
                project_results.project_name = form.cleaned_data['project_name']
                project_results.project_description = form.cleaned_data['project_description']
                project_results.project_start_date = form.cleaned_data['project_start_date']
                project_results.project_end_date = form.cleaned_data['project_end_date']
                if 'Resolve' in request.POST:
                    project_results.project_status = 'Closed'
                project_results.change_user = request.user
                project_results.save()
                kanban_card_results = kanban_card.objects.filter(is_deleted='FALSE',
                  project_id=project_id)
                for row in kanban_card_results:
                    row.kanban_card_text = 'PRO' + str(project_id) + ' - ' + form.cleaned_data['project_name']
                    row.save()

        else:
            print(form.errors)
    project_results = get_object_or_404(project, project_id=project_id)
    opportunity_results = opportunity.objects.filter(is_deleted='FALSE',
      opportunity_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id).values('project_id')))
    if project_results.project_status == 'Closed':
        return HttpResponseRedirect(reverse('project_readonly', args={project_id}))
    project_history_results = project_history.objects.filter(project_id=project_id, is_deleted='FALSE')
    cursor = connection.cursor()
    requirement_results = requirement.objects.filter(is_deleted='FALSE',
      requirement_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id,
      requirement_id__isnull=False).values('requirement_id')))
    requirement_item_results = requirement_item.objects.filter(is_deleted='FALSE',
      requirement_item_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id,
      requirement_item_id__isnull=False).values('requirement_item_id')))
    folders_results = folder.objects.filter(project_id=project_id,
      is_deleted='FALSE').order_by('folder_description')
    initial = {'project_name':project_results.project_name, 
     'project_description':project_results.project_description, 
     'project_start_date':project_results.project_start_date, 
     'project_end_date':project_results.project_end_date}
    associated_task_results = task.objects.filter(is_deleted='FALSE',
      task_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id).values('task_id')))
    quote_results = quote.objects.filter(is_deleted='FALSE',
      project_id=project_results)
    t = loader.get_template('NearBeach/project_information.html')
    c = {'project_information_form':project_information_form(initial=initial), 
     'information_project_history_form':information_project_history_form(), 
     'project_results':project_results, 
     'associated_task_results':associated_task_results, 
     'project_history_results':project_history_results, 
     'folders_results':serializers.serialize('json', folders_results), 
     'media_url':settings.MEDIA_URL, 
     'quote_results':quote_results, 
     'project_id':project_id, 
     'permission':permission_results['project'], 
     'project_history_permissions':permission_results['project_history'], 
     'timezone':settings.TIME_ZONE, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'opportunity_results':opportunity_results, 
     'requirement_results':requirement_results, 
     'requirement_item_results':requirement_item_results, 
     'open_status':[
      'New', 'Open', 'Backlog']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def project_readonly(request, project_id):
    project_groups_results = object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project.objects.get(project_id=project_id)).values('group_id_id')
    permission_results = return_user_permission_level(request, project_groups_results, ['project', 'project_history'])
    project_results = project.objects.get(project_id=project_id)
    to_do_results = to_do.objects.filter(is_deleted='FALSE',
      project_id=project_id)
    project_history_results = project_history.objects.filter(is_deleted='FALSE',
      project_id=project_id)
    requirement_results = requirement.objects.filter(is_deleted='FALSE',
      requirement_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id).values('requirement_id')))
    requirement_item_results = requirement_item.objects.filter(is_deleted='FALSE',
      requirement_item_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id).values('requirement_item_id')))
    email_results = email_content.objects.filter(is_deleted='FALSE',
      email_content_id__in=(email_contact.objects.filter(Q(project=project_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
    associated_tasks_results = object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id,
      task_id__isnull=False)
    project_customer_results = project_customer.objects.filter(is_deleted='FALSE',
      project_id=project_id)
    costs_results = cost.objects.filter(project_id=project_id,
      is_deleted='FALSE')
    quote_results = quote.objects.filter(is_deleted='FALSE',
      project_id=project_id)
    bug_results = bug.objects.filter(is_deleted='FALSE',
      project_id=project_id)
    assigned_results = object_assignment.objects.filter(project_id=project_id,
      is_deleted='FALSE').exclude(assigned_user=None).values('assigned_user__id', 'assigned_user', 'assigned_user__username', 'assigned_user__first_name', 'assigned_user__last_name').distinct()
    group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
      project_id=project_id)
    kudos_results = kudos.objects.filter(project_id=project_id,
      is_deleted='FALSE')
    project_history_collective = []
    for row in project_history_results:
        project_history_collective.append(project_history_readonly_form(initial={'project_history':row.project_history, 
         'submit_history':row.user_infomation + ' - ' + str(row.user_id) + ' - ' + row.date_created.strftime('%d %B %Y %H:%M.%S')},
          project_history_id=(row.project_history_id)))

    t = loader.get_template('NearBeach/project_information/project_readonly.html')
    c = {'project_id':project_id, 
     'project_results':project_results, 
     'project_readonly_form':project_readonly_form(initial={'project_description': project_results.project_description}), 
     'kudos_results':kudos_results, 
     'to_do_results':to_do_results, 
     'project_history_collective':project_history_collective, 
     'email_results':email_results, 
     'associated_tasks_results':associated_tasks_results, 
     'project_customer_results':project_customer_results, 
     'costs_results':costs_results, 
     'quote_results':quote_results, 
     'bug_results':bug_results, 
     'assigned_results':assigned_results, 
     'group_list_results':group_list_results, 
     'project_permissions':permission_results['project'], 
     'project_history_permissions':permission_results['project_history'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'requirement_results':requirement_results, 
     'requirement_item_results':requirement_item_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def project_remove_customer(request, project_customer_id):
    if request.method == 'POST':
        project_customer_update = project_customer.objects.get(project_customer_id=project_customer_id)
        project_customer_update.is_deleted = 'TRUE'
        project_customer_update.change_user = request.user
        project_customer_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Can only do this through POST')


@login_required(login_url='login', redirect_field_name='')
def quote_information(request, quote_id):
    permission_results = return_user_permission_level(request, None, 'quote')
    if permission_results['quote'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    quotes_results = quote.objects.get(quote_id=quote_id)
    print('QUOTE STAGE: ' + str(quotes_results.quote_stage_id))
    if not quotes_results.quote_stage_id.quote_closed == 'TRUE':
        if permission_results['quote'] == 1:
            return HttpResponseRedirect(reverse('quote_readonly', args={quote_id}))
        quote_template_results = quote_template.objects.filter(is_deleted='FALSE')
        if quotes_results.customer_id or quotes_results.organisation_id:
            cust_or_org_connected = True
        else:
            cust_or_org_connected = False
        if request.method == 'POST':
            form = quote_information_form((request.POST), quote_instance=quotes_results)
            if form.is_valid():
                quotes_results.quote_title = form.cleaned_data['quote_title']
                quotes_results.quote_terms = form.cleaned_data['quote_terms']
                quotes_results.quote_stage_id = form.cleaned_data['quote_stage_id']
                quotes_results.customer_notes = form.cleaned_data['customer_notes']
                quotes_results.quote_billing_address = form.cleaned_data['quote_billing_address']
                quotes_results.quote_valid_till = form.cleaned_data['quote_valid_till']
                if 'create_invoice' in request.POST:
                    quotes_results.is_invoice = 'TRUE'
                    quotes_results.quote_stage_id = list_of_quote_stage.objects.filter(is_invoice='TRUE').order_by('sort_order')[0]
                if 'revert_quote' in request.POST:
                    quotes_results.is_invoice = 'FALSE'
                    quotes_results.quote_stage_id = list_of_quote_stage.objects.filter(is_invoice='FALSE').order_by('sort_order')[0]
                quotes_results.change_user = request.user
                quotes_results.save()
        else:
            print(form.errors)
    else:
        user_groups_results = user_group.objects.filter(username=(request.user))
        quote_permission_results = object_assignment.objects.filter(Q(Q(assigned_user=(request.user)) | Q(group_id__in=(user_groups_results.values('group_id')))) & Q(quote_id=quote_id) & Q(is_deleted='FALSE'))
        if not quote_permission_results:
            return HttpResponseRedirect(reverse(permission_denied))
        quote_or_invoice = 'Quote'
        if quotes_results.is_invoice == 'TRUE':
            quote_or_invoice = 'Invoice'
        quote_valid_till_hour = quotes_results.quote_valid_till.hour
        quote_valid_till_meridiem = 'AM'
    if quote_valid_till_hour == 0:
        quote_valid_till_hour = 12
    else:
        if quote_valid_till_hour == 12:
            quote_valid_till_meridiem = 'PM'
        else:
            if quote_valid_till_hour > 12:
                start_hour = quote_valid_till_hour - 12
                quote_valid_till_meridiem = 'PM'
            initial = {'quote_title':quotes_results.quote_title, 
             'quote_terms':quotes_results.quote_terms, 
             'quote_stage_id':quotes_results.quote_stage_id.quote_stage_id, 
             'quote_valid_till_year':quotes_results.quote_valid_till.year, 
             'quote_valid_till_month':quotes_results.quote_valid_till.month, 
             'quote_valid_till_day':quotes_results.quote_valid_till.day, 
             'quote_valid_till_hour':quote_valid_till_hour, 
             'quote_valid_till_minute':quotes_results.quote_valid_till.minute, 
             'quote_valid_till_meridiem':quote_valid_till_meridiem, 
             'customer_notes':quotes_results.customer_notes, 
             'quote_billing_address':quotes_results.quote_billing_address}
            t = loader.get_template('NearBeach/quote_information.html')
            c = {'quotes_results':quotes_results, 
             'quote_information_form':quote_information_form(initial=initial,
               quote_instance=quotes_results), 
             'quote_id':quote_id, 
             'cust_or_org_connected':cust_or_org_connected, 
             'quote_or_invoice':quote_or_invoice, 
             'timezone':settings.TIME_ZONE, 
             'quote_template_results':quote_template_results, 
             'permission':permission_results['quote'], 
             'new_item_permission':permission_results['new_item'], 
             'administration_permission':permission_results['administration']}
            return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def quote_template_information(request, quote_template_id):
    permission_results = return_user_permission_level(request, None, 'template')
    if permission_results['template'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
        if request.method == 'POST':
            form = quote_template_form(request.POST)
            if form.is_valid():
                quote_template_save = quote_template.objects.get(quote_template_id=quote_template_id)
                quote_template_save.change_user = request.user
                quote_template_save.quote_template_description = form.cleaned_data['quote_template_description']
                quote_template_save.template_css = form.cleaned_data['template_css']
                quote_template_save.header = form.cleaned_data['header']
                quote_template_save.company_letter_head = form.cleaned_data['company_letter_head']
                quote_template_save.payment_terms = form.cleaned_data['payment_terms']
                quote_template_save.notes = form.cleaned_data['notes']
                quote_template_save.organisation_details = form.cleaned_data['organisation_details']
                quote_template_save.payment_method = form.cleaned_data['payment_method']
                quote_template_save.footer = form.cleaned_data['footer']
                quote_template_save.page_layout = form.cleaned_data['page_layout']
                quote_template_save.margin_left = form.cleaned_data['margin_left']
                quote_template_save.margin_right = form.cleaned_data['margin_right']
                quote_template_save.margin_top = form.cleaned_data['margin_top']
                quote_template_save.margin_bottom = form.cleaned_data['margin_bottom']
                quote_template_save.margin_header = form.cleaned_data['margin_header']
                quote_template_save.margin_footer = form.cleaned_data['margin_footer']
                if request.POST.get('delete_quote_template'):
                    quote_template_save.is_deleted = 'TRUE'
                    quote_template_save.save()
                    return HttpResponseRedirect(reverse(search_templates))
                quote_template_save.save()
    else:
        print(form.errors)
    quote_template_results = quote_template.objects.get(quote_template_id=quote_template_id)
    t = loader.get_template('NearBeach/quote_template_information.html')
    c = {'quote_template_form':quote_template_form(initial={'quote_template_description':quote_template_results.quote_template_description, 
      'template_css':quote_template_results.template_css, 
      'header':quote_template_results.header, 
      'company_letter_head':quote_template_results.company_letter_head, 
      'payment_terms':quote_template_results.payment_terms, 
      'notes':quote_template_results.notes, 
      'organisation_details':quote_template_results.organisation_details, 
      'product_line':quote_template_results.product_line, 
      'service_line':quote_template_results.service_line, 
      'payment_method':quote_template_results.payment_method, 
      'footer':quote_template_results.footer, 
      'page_layout':quote_template_results.page_layout, 
      'margin_left':quote_template_results.margin_left, 
      'margin_right':quote_template_results.margin_right, 
      'margin_top':quote_template_results.margin_top, 
      'margin_bottom':quote_template_results.margin_bottom, 
      'margin_header':quote_template_results.margin_header, 
      'margin_footer':quote_template_results.margin_footer}), 
     'quote_template_id':quote_template_id, 
     'quote_permission':permission_results['template'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def quote_readonly(request, quote_id):
    permission_results = return_user_permission_level(request, None, 'quote')
    if permission_results['quote'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    quote_results = quote.objects.get(quote_id=quote_id)
    line_item_results = quote_product_and_service.objects.filter(is_deleted='FALSE',
      quote_id=quote_id)
    product_line_items = quote_product_and_service.objects.filter(quote_id=quote_id,
      product_and_service__product_or_service='Product',
      is_deleted='FALSE')
    service_line_items = quote_product_and_service.objects.filter(quote_id=quote_id,
      product_and_service__product_or_service='Service',
      is_deleted='FALSE')
    responsible_customer_results = customer.objects.filter(customer_id__in=(quote_responsible_customer.objects.filter(quote_id=quote_id,
      is_deleted='FALSE').values('customer_id').distinct()))
    email_results = email_content.objects.filter(is_deleted='FALSE',
      email_content_id__in=(email_contact.objects.filter(Q(quotes=quote_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
    quote_template_results = quote_template.objects.filter(is_deleted='FALSE')
    group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
      quote_id=quote_id).exclude(group_id=None)
    assigned_user_results = object_assignment.objects.filter(is_deleted='FALSE',
      quote_id=quote_id).exclude(assigned_user=None)
    t = loader.get_template('NearBeach/quote_information/quote_readonly.html')
    c = {'quote_results':quote_results, 
     'quote_readonly_form':quote_readonly_form(initial={'quote_terms':quote_results.quote_terms, 
      'customer_notes':quote_results.customer_notes}), 
     'timezone':settings.TIME_ZONE, 
     'line_item_results':line_item_results, 
     'product_line_items':product_line_items, 
     'service_line_items':service_line_items, 
     'responsible_customer_results':responsible_customer_results, 
     'email_results':email_results, 
     'quote_template_results':quote_template_results, 
     'group_list_results':group_list_results, 
     'assigned_user_results':assigned_user_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def rename_document(request, document_key):
    if request.method == 'POST':
        print(request)
    else:
        return HttpResponseBadRequest('This is a POST function. POST OFF!')


@login_required(login_url='login', redirect_field_name='')
def request_for_change_approve(request, rfc_id):
    """
    The user has requested to approve their request for change. This will process that request
    :param request:
    :param rfc_id: The request for change we are submitting
    :return: Blank page

    Method
    ~~~~~~
    1. Check that the method is in POST
    2. Check to make sure the user has permission to submit the rfc
    3. Change the request for change group approval to approved
    4. Check the approval status of the request for change
    5. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'request_for_change')
        if permission_results['request_for_change'] <= 2:
            return HttpResponseRedirect(reverse('permission_denied'))
        request_for_change_group_approval.objects.filter(is_deleted='FALSE',
          rfc_id=rfc_id,
          group_id__in=(user_group.objects.filter(is_deleted='FALSE',
          group_leader=True,
          username=(request.user)).values('group_id')),
          approval=1).update(approval=2)
        check_approval_status(rfc_id)
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - has to be done in POST')


@login_required(login_url='login', redirect_field_name='')
def request_for_change_draft(request, rfc_id):
    """
    This is the section where the user can edit the draft of their RFC.
    :param request:
    :param rfc_id: The draft for this RFC
    :return: Web page

    Method
    ~~~~~~
    1. Check permissions
    2. Check to make sure RFC is in draft mode - otherwise send them to the information page
    3. Check the method - if POST look at method there
    3. Get data
    4. Get template
    5. Render results
    """
    permission_results = return_user_permission_level(request, None, 'request_for_change')
    if permission_results['request_for_change'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        if not rfc_results.rfc_status == 1:
            return HttpResponseRedirect(reverse('request_for_change_information', args={rfc_id}))
        print('METHOD')
        print(request.method)
        if request.method == 'POST':
            form = request_for_change_form(request.POST)
            if form.is_valid():
                rfc_results.rfc_title = form.cleaned_data['rfc_title']
                rfc_results.rfc_summary = form.cleaned_data['rfc_summary']
                rfc_results.rfc_type = form.cleaned_data['rfc_type']
                rfc_results.rfc_implementation_start_date = form.cleaned_data['rfc_implementation_start_date']
                rfc_results.rfc_implementation_end_date = form.cleaned_data['rfc_implementation_end_date']
                rfc_results.rfc_implementation_release_date = form.cleaned_data['rfc_implementation_release_date']
                rfc_results.rfc_version_number = form.cleaned_data['rfc_version_number']
                rfc_results.rfc_lead = form.cleaned_data['rfc_lead']
                rfc_results.rfc_priority = form.cleaned_data['rfc_priority']
                rfc_results.rfc_risk = form.cleaned_data['rfc_risk']
                rfc_results.rfc_impact = form.cleaned_data['rfc_impact']
                rfc_results.rfc_risk_and_impact_analysis = form.cleaned_data['rfc_risk_and_impact_analysis']
                rfc_results.rfc_implementation_plan = form.cleaned_data['rfc_implementation_plan']
                rfc_results.rfc_backout_plan = form.cleaned_data['rfc_backout_plan']
                rfc_results.rfc_test_plan = form.cleaned_data['rfc_test_plan']
                rfc_results.save()
    else:
        print(form.errors)
    organisation_stakeholders = organisation.objects.filter(is_deleted='FALSE',
      organisation_id__in=(request_for_change_stakeholder.objects.filter(is_deleted='FALSE',
      request_for_change=rfc_id,
      organisation_id__isnull=False).values('organisation_id')))
    customer_stakeholders = customer.objects.filter(is_deleted='FALSE',
      customer_id__in=(request_for_change_stakeholder.objects.filter(is_deleted='FALSE',
      request_for_change=rfc_id,
      customer_id__isnull=False).values('customer_id')))
    t = loader.get_template('NearBeach/request_for_change_draft.html')
    c = {'request_for_change_form':request_for_change_form(initial={'rfc_title':rfc_results.rfc_title, 
      'rfc_type':rfc_results.rfc_type, 
      'rfc_implementation_start_date':rfc_results.rfc_implementation_start_date, 
      'rfc_implementation_end_date':rfc_results.rfc_implementation_end_date, 
      'rfc_implementation_release_date':rfc_results.rfc_implementation_release_date, 
      'rfc_version_number':rfc_results.rfc_version_number, 
      'rfc_summary':rfc_results.rfc_summary, 
      'rfc_lead':rfc_results.rfc_lead, 
      'rfc_priority':rfc_results.rfc_priority, 
      'rfc_risk':rfc_results.rfc_risk, 
      'rfc_impact':rfc_results.rfc_impact, 
      'rfc_risk_and_impact_analysis':rfc_results.rfc_risk_and_impact_analysis, 
      'rfc_implementation_plan':rfc_results.rfc_implementation_plan, 
      'rfc_backout_plan':rfc_results.rfc_backout_plan, 
      'rfc_test_plan':rfc_results.rfc_test_plan}), 
     'organisation_stakeholders':organisation_stakeholders, 
     'customer_stakeholders':customer_stakeholders, 
     'rfc_results':rfc_results, 
     'permission':permission_results['request_for_change'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def request_for_change_finish(request, rfc_id):
    """
    This function will only be called during the request_for_change_start. This function is designed to show NOTHING
    until the user has completed all of their change tasks. Once all change tasks have been completed a simple form
    will appear allowing the user to close the RFC.

    The GET method renders the form
    The POST method finishes the RFC and sends the user to the request_for_change_information page
    :param request:
    :param rfc_id:
    :return:

    Method
    ~~~~~~
    1. Check to see which method the user is using. The POST method instructions will be displayed in the IF statement
    2. Count how many change tasks are left for this rfc
    3. Get template, context, and render
    """
    if request.method == 'POST':
        request_for_change.objects.filter(rfc_id=rfc_id).update(rfc_status=5)
        return HttpResponseRedirect(reverse('request_for_change_information', args={rfc_id}))
    change_task_count = change_task.objects.filter(is_deleted='FALSE',
      request_for_change_id=rfc_id,
      change_task_status__in=[
     1, 2, 3, 4]).count()
    t = loader.get_template('NearBeach/request_for_change/request_for_change_finish.html')
    c = {'rfc_id':rfc_id, 
     'change_task_count':change_task_count}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def request_for_change_information(request, rfc_id):
    """
    The request for change information is a READ ONLY section. If the RFC is in draft then it will send the user to the
    request_for_change_draft module where the user can edit the form.
    :param request:
    :param rfc_id:
    :return:
    """
    permission_results = return_user_permission_level(request, None, 'request_for_change')
    if permission_results['request_for_change'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    else:
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        organisation_stakeholders = organisation.objects.filter(is_deleted='FALSE',
          organisation_id__in=(request_for_change_stakeholder.objects.filter(is_deleted='FALSE',
          request_for_change=rfc_id,
          organisation_id__isnull=False).values('organisation_id')))
        customer_stakeholders = customer.objects.filter(is_deleted='FALSE',
          customer_id__in=(request_for_change_stakeholder.objects.filter(is_deleted='FALSE',
          request_for_change=rfc_id,
          customer_id__isnull=False).values('customer_id')))
        group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
          request_for_change=rfc_id).exclude(group_id=None)
        change_task_results = change_task.objects.filter(is_deleted='FALSE',
          request_for_change=rfc_id).order_by('change_task_start_date', 'change_task_end_date', 'change_task_assigned_user', 'change_task_qa_user')
        assigned_user_results = User.objects.filter(is_active=True,
          id__in=(change_task_results.values('change_task_assigned_user')))
        qa_user_results = User.objects.filter(is_active=True,
          id__in=(change_task_results.values('change_task_qa_user')))
        if rfc_results.rfc_status == 2:
            object_assignment_results = object_assignment.objects.filter(is_deleted='FALSE',
              request_for_change=rfc_id,
              group_id__in=(user_group.objects.filter(is_deleted='FALSE',
              group_leader='TRUE',
              username=(request.user)).values('group_id'))).values('request_for_change')
            if object_assignment_results:
                team_leader = True
            else:
                team_leader = False
            group_approval_results = request_for_change_group_approval.objects.filter(is_deleted='FALSE',
              rfc_id=rfc_id)
        else:
            team_leader = False
            group_approval_results = ''
        if rfc_results.rfc_status == 4:
            t = loader.get_template('NearBeach/request_for_change_start.html')
        else:
            t = loader.get_template('NearBeach/request_for_change_information.html')
    c = {'rfc_form':request_for_change_readonly_form(initial={'rfc_summary':rfc_results.rfc_summary, 
      'rfc_risk_and_impact_analysis':rfc_results.rfc_risk_and_impact_analysis, 
      'rfc_implementation_plan':rfc_results.rfc_implementation_plan, 
      'rfc_backout_plan':rfc_results.rfc_backout_plan, 
      'rfc_test_plan':rfc_results.rfc_test_plan}), 
     'team_leader':team_leader, 
     'request_for_change_note_form':request_for_change_note_form, 
     'group_approval_results':group_approval_results, 
     'change_task_results':change_task_results, 
     'assigned_user_results':assigned_user_results, 
     'qa_user_results':qa_user_results, 
     'group_list_results':group_list_results, 
     'organisation_stakeholders':organisation_stakeholders, 
     'customer_stakeholders':customer_stakeholders, 
     'rfc_results':rfc_results, 
     'permission':permission_results['request_for_change'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'RFC_IMPACT':dict(RFC_IMPACT)[rfc_results.rfc_impact], 
     'RFC_PRIORITY':dict(RFC_PRIORITY)[rfc_results.rfc_priority], 
     'RFC_RISK':dict(RFC_RISK)[rfc_results.rfc_risk], 
     'RFC_STATUS':dict(RFC_STATUS)[rfc_results.rfc_status], 
     'RFC_TYPE':dict(RFC_TYPE)[rfc_results.rfc_type]}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def request_for_change_reject(request, rfc_id):
    """
    The user has requested to reject their request for change. This will process that request
    :param request:
    :param rfc_id: The request for change we are submitting
    :return: Blank page

    Method
    ~~~~~~
    1. Check that the method is in POST
    2. Check to make sure the user has permission to submit the rfc
    3. Change the request to rejected
    4. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'request_for_change')
        if permission_results['request_for_change'] <= 2:
            return HttpResponseRedirect(reverse('permission_denied'))
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        rfc_results.rfc_status = 6
        rfc_results.save()
        request_for_change_group_approval.objects.filter(is_deleted='FALSE',
          approval=1,
          rfc_id=rfc_id).update(approval=3)
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - has to be done in POST')


@login_required(login_url='login', redirect_field_name='')
def request_for_change_set_to_draft(request, rfc_id):
    """
    The user has requested to set back to draft. This will process that request
    :param request:
    :param rfc_id: The request for change we are submitting
    :return: Blank page

    Method
    ~~~~~~
    1. Check that the method is in POST
    2. Check to make sure the user has permission to submit the rfc
    3. Change the request to draft
    4. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'request_for_change')
        if permission_results['request_for_change'] <= 2:
            return HttpResponseRedirect(reverse('permission_denied'))
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        rfc_results.rfc_status = 1
        rfc_results.save()
        request_for_change_group_approval.objects.filter(is_deleted='FALSE',
          approval=1,
          rfc_id=rfc_id).update(approval=4)
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - has to be done in POST')


@login_required(login_url='login', redirect_field_name='')
def request_for_change_start(request, rfc_id):
    """
    The user has requested the rfc to start. This will process that request
    :param request:
    :param rfc_id: The request for change we are submitting
    :return: Blank page

    Method
    ~~~~~~
    1. Check that the method is in POST
    2. Check to make sure the user has permission to submit the rfc
    3. Change the start
    4. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'request_for_change')
        if permission_results['request_for_change'] <= 2:
            return HttpResponseRedirect(reverse('permission_denied'))
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        rfc_results.rfc_status = 4
        rfc_results.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - has to be done in POST')


@login_required(login_url='login', redirect_field_name='')
def request_for_change_submit(request, rfc_id):
    """
    The user has requested to submit their request for change for approval. This will process that request
    :param request:
    :param rfc_id: The request for change we are submitting
    :return: Blank page

    Method
    ~~~~~~
    1. Check that the method is in POST
    2. Check to make sure the user has permission to submit the rfc
    3. Change the request to waiting for approval
    4. Return blank page
    """
    if request.method == 'POST':
        permission_results = return_user_permission_level(request, None, 'request_for_change')
        if permission_results['request_for_change'] <= 2:
            return HttpResponseRedirect(reverse('permission_denied'))
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        rfc_results.rfc_status = 2
        rfc_results.save()
        rfc_group_results = object_assignment.objects.filter(is_deleted='FALSE',
          request_for_change=(rfc_results.rfc_id),
          group_id__isnull=False)
        for row in rfc_group_results:
            submit_rfc_group_approval = request_for_change_group_approval(rfc_id=rfc_results,
              group_id=(row.group_id),
              change_user=(request.user))
            group_leader = user_group.objects.filter(is_deleted='FALSE',
              group_id=(row.group_id),
              group_leader='TRUE').count()
            if group_leader == 0:
                submit_rfc_group_approval.approval = 2
            submit_rfc_group_approval.save()

        check_approval = request_for_change_group_approval.objects.filter(Q(is_deleted='FALSE',
          rfc_id=(rfc_results.rfc_id)) & ~Q(approval=2)).count()
        if check_approval == 0:
            rfc_results.rfc_status = 3
            rfc_results.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry - has to be done in POST')


@login_required(login_url='login', redirect_field_name='')
def resolve_project(request, project_id):
    project_update = project.objects.get(project_id=project_id)
    project_update.project_status = 'Closed'
    project_update.change_user = request.user
    project_update.save()
    return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url='login', redirect_field_name='')
def resolve_task(request, task_id):
    task_update = task.objects.get(task_id=task_id)
    task_update.task_status = 'Closed'
    task_update.change_user = request.user
    task_update.save()
    return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url='login', redirect_field_name='')
def search(request):
    permission_results = return_user_permission_level(request, None, 'project')
    t = loader.get_template('NearBeach/search.html')
    search_results = ''
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            search_results = form.cleaned_data['search_for']
    search_like = '%'
    for split_row in search_results.split(' '):
        search_like += split_row
        search_like += '%'

    int_results = 0
    if not search_results == '':
        if isinstance(search_results, int):
            int_results = int(search_results)
    project_results = project.objects.extra(where=[
     '\n            project_id = %s\n            OR project_name LIKE %s\n            OR project_description LIKE %s\n            ',
     '\n            is_deleted="FALSE"\n            '],
      params=[
     int(int_results),
     search_like,
     search_like])
    task_results = task.objects.extra(where=[
     '\n            task_id = %s\n            OR task_short_description LIKE %s\n            OR task_long_description LIKE %s\n            ',
     '\n            is_deleted="FALSE"\n            '],
      params=[
     int(int_results),
     search_like,
     search_like])
    opportunity_results = opportunity.objects.all()
    requirement_results = requirement.objects.all()
    rfc_results = request_for_change.objects.all()
    c = {'search_form':search_form(initial={'search_for': search_results}), 
     'project_results':project_results, 
     'task_results':task_results, 
     'opportunity_results':opportunity_results, 
     'requirement_results':requirement_results, 
     'rfc_results':rfc_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_customer(request):
    permission_results = return_user_permission_level(request, None, 'customer')
    t = loader.get_template('NearBeach/search_customer.html')
    search_customer_results = ''
    if request.method == 'POST':
        form = search_customer_form(request.POST)
        if form.is_valid():
            search_customer_results = form.cleaned_data['search_customer']
    customer_results = customer.objects.filter(is_deleted='FALSE')
    for split_row in search_customer_results.split(' '):
        customer_results = customer_results.filter(Q(customer_first_name__contains=split_row) | Q(customer_last_name__contains=split_row))

    c = {'search_customer_form':search_customer_form(initial={'search_customer': search_customer_results}), 
     'customer_results':customer_results, 
     'customer_permission':permission_results['customer'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_group(request):
    """
    Brings up a list of all groups.
    :param request:
    :return:
    """
    permission_results = return_user_permission_level(request, None, 'administration_create_group')
    if permission_results['administration_create_group'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    group_results = group.objects.filter(is_deleted='FALSE')
    t = loader.get_template('NearBeach/search_group.html')
    c = {'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'group_results':group_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_kanban(request):
    permission_results = return_user_permission_level(request, None, ['kanban'])
    if permission_results['kanban'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    kanban_form = search_kanban_form(None or request.POST)
    kanban_search_results = ''
    if request.method == 'POST':
        if kanban_form.is_valid():
            kanban_search_results = kanban_form.cleaned_data['search_kanban']
    kanban_board_results = kanban_board.objects.filter(is_deleted='FALSE',
      kanban_board_status='Open')
    for split_row in kanban_search_results.split(' '):
        kanban_board_results = kanban_board_results.filter(kanban_board_name__contains=split_row)

    t = loader.get_template('NearBeach/search_kanban.html')
    c = {'search_kanban_form':kanban_form, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'kanban_permission':permission_results['kanban'], 
     'kanban_board_results':kanban_board_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_organisation(request):
    permission_results = return_user_permission_level(request, None, 'organisation')
    t = loader.get_template('NearBeach/search_organisations.html')
    search_organisation_results = ''
    if request.method == 'POST':
        form = search_organisation_form(request.POST)
        if form.is_valid():
            search_organisation_results = form.cleaned_data['search_organisation']
    organisation_results = organisation.objects.filter(is_deleted='FALSE')
    for split_row in search_organisation_results.split(' '):
        organisation_results = organisation_results.filter(organisation_name__contains=split_row)

    c = {'search_organisation_form':search_organisation_form(initial={'search_organisation': search_organisation_results}), 
     'organisation_results':organisation_results, 
     'organisation_permission':permission_results['organisation'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_permission_set(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_set')
    if permission_results['administration_create_permission_set'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    permission_set_results = permission_set.objects.filter(is_deleted='FALSE')
    t = loader.get_template('NearBeach/search_permission_set.html')
    c = {'permission_set_results':permission_set_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_projects_task(request):
    t = loader.get_template('NearBeach/search_projects_and_task.html')
    print('Search project and task')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_tags(request):
    """
    This search functionality allows the user to search NearBeach for tags. Tags are connected to the objects;
    - Projects
    - Tasks
    - Requirements
    - Opportunities

    This will bring back a result of ALL objects that contain that tag
    :param request:
    :return:

    Method
    ~~~~~~
    1. Check permissions - if you do not have permissions then you will be carted away
    2. Declare all variables
    3. Check to see if this is in POST
    """
    permission_results = return_user_permission_level(request, None, 'tag')
    if permission_results['tag'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    search_for = ''
    search_form_form = search_form(request.POST or None)
    if request.method == 'POST':
        if search_form_form.is_valid():
            search_for = search_form_form.cleaned_data['search_for']
    tag_assignment_results = tag_assignment.objects.filter(is_deleted='FALSE',
      tag_id__in=(tag.objects.filter(is_deleted='FALSE',
      tag_name__contains=search_for).values('tag_id')))
    project_results = project.objects.filter(Q(is_deleted='FALSE') and Q(project_id__in=(object_assignment.objects.filter(Q(is_deleted='FALSE') and Q(Q(assigned_user_id=(request.user.id)) or Q(group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id'))))).values('project_id'))) and Q(project_id__in=(tag_assignment_results.filter(project_id__isnull=False).values('project_id'))))
    task_results = task.objects.filter(Q(is_deleted='FALSE') and Q(task_id__in=(object_assignment.objects.filter(Q(is_deleted='FALSE') and Q(Q(assigned_user_id=(request.user.id)) or Q(group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id'))))).values('task_id'))) and Q(task_id__in=(tag_assignment_results.filter(task_id__isnull=False).values('task_id'))))
    requirement_results = requirement.objects.filter(Q(is_deleted='FALSE') and Q(requirement_id__in=(object_assignment.objects.filter(Q(is_deleted='FALSE') and Q(Q(assigned_user_id=(request.user.id)) or Q(group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id'))))).values('requirement_id'))) and Q(requirement_id__in=(tag_assignment_results.filter(requirement_id__isnull=False).values('requirement_id'))))
    opportunity_results = opportunity.objects.filter(Q(is_deleted='FALSE') and Q(opportunity_id__in=(object_assignment.objects.filter(Q(is_deleted='FALSE') and Q(Q(assigned_user_id=(request.user.id)) or Q(group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id'))))).values('opportunity_id'))) and Q(opportunity_id__in=(tag_assignment_results.filter(opportunity_id__isnull=False).values('opportunity_id'))))
    t = loader.get_template('NearBeach/search_tags.html')
    c = {'search_form':search_form_form, 
     'project_results':project_results, 
     'task_results':task_results, 
     'requirement_results':requirement_results, 
     'opportunity_results':opportunity_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_templates(request):
    permission_results = return_user_permission_level(request, None, 'templates')
    if permission_results['templates'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    quote_template_results = quote_template.objects.filter(is_deleted='FALSE')
    t = loader.get_template('NearBeach/search_templates.html')
    print('Search templates')
    c = {'quote_template_results':quote_template_results, 
     'search_template_form':search_template_form(), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def tag_information(request, location_id, destination):
    """
    Tag information is where the user requests tags for certain objects.

    :param request:
    :param location_id: the object id
    :param destination: the type of object, i.e. project, task, requirement, or opportunity
    :return: HTML for tag information

    Method
    ~~~~~~
    1. Check user permissions
    2. If POST, check comments in section - because it will save the tag
    3. Check which object type we are requesting for
    4. Gather the required data
    5. Send data to template and render
    6. Give the HTML to user. YAY :D
    """
    permission_results = return_user_permission_level(request, None, 'tag')
    if request.method == 'POST':
        form = new_tag_form(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['tag_name']
            tag_instance = tag.objects.filter(tag_name=tag_name)
            if not tag_instance:
                tag_submit = tag(tag_name=tag_name,
                  change_user=(request.user))
                tag_submit.save()
                tag_instance = tag_submit
            else:
                tag_instance = tag_instance[0]
                if tag_instance.is_deleted == 'TRUE':
                    tag_instance.is_deleted = 'FALSE'
                    tag_instance.save()
                else:
                    tag_assignment_submit = tag_assignment(tag_id=tag_instance,
                      change_user=(request.user))
                    if destination == 'project':
                        tag_assignment_submit.project_id = project.objects.get(project_id=location_id)
                    else:
                        if destination == 'task':
                            tag_assignment_submit.task_id = task.objects.get(task_id=location_id)
                        else:
                            if destination == 'opportunity':
                                tag_assignment_submit.opportunity_id = opportunity.objects.get(opportunity_id=location_id)
                            else:
                                if destination == 'requirement':
                                    tag_assignment_submit.requirement_id = requirement.objects.get(requirement_id=location_id)
                tag_assignment_submit.save()
        else:
            print(form.errors)
    elif destination == 'project':
        tag_results = tag.objects.filter(is_deleted='FALSE',
          tag_id__in=(tag_assignment.objects.filter(is_deleted='FALSE',
          project_id=location_id).values('tag_id')))
    else:
        if destination == 'task':
            tag_results = tag.objects.filter(is_deleted='FALSE',
              tag_id__in=(tag_assignment.objects.filter(is_deleted='FALSE',
              task_id=location_id).values('tag_id')))
        else:
            if destination == 'opportunity':
                tag_results = tag.objects.filter(is_deleted='FALSE',
                  tag_id__in=(tag_assignment.objects.filter(is_deleted='FALSE',
                  opportunity_id=location_id).values('tag_id')))
            else:
                if destination == 'requirement':
                    tag_results = tag.objects.filter(is_deleted='FALSE',
                      tag_id__in=(tag_assignment.objects.filter(is_deleted='FALSE',
                      requirement_id=location_id).values('tag_id')))
                else:
                    tag_results = None
    tag_list_results = tag.objects.filter(is_deleted='FALSE').exclude(tag_id__in=(tag_results.values('tag_id')))
    t = loader.get_template('NearBeach/tag_information.html')
    c = {'tag_results':tag_results, 
     'new_tag_form':new_tag_form(), 
     'tag_permission':permission_results['tag']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def task_information(request, task_id):
    group_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id,
      group_id__isnull=False).values('group_id')
    permission_results = return_user_permission_level(request, group_results, ['task', 'task_history'])
    if permission_results['task'] == 0:
        return HttpResponseRedirect(reverse(permission_denied))
    object_access = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id,
      group_id__in=(user_group.objects.filter(is_deleted='FALSE',
      username=(request.user)).values('group_id')))
    if object_access.count() == 0:
        if not permission_results['administration'] == 4:
            return HttpResponseRedirect(reverse('permission_denied'))
    task_results = get_object_or_404(task, task_id=task_id)
    if task_results.task_status in 'Closed' or permission_results['task'] == 1:
        return HttpResponseRedirect(reverse('task_readonly', args={task_id}))
    if request.method == 'POST':
        form = task_information_form(request.POST, request.FILES)
        if form.is_valid():
            task_results.task_short_description = form.cleaned_data['task_short_description']
            task_results.task_long_description = form.cleaned_data['task_long_description']
            task_results.task_start_date = form.cleaned_data['task_start_date']
            task_results.task_end_date = form.cleaned_data['task_end_date']
            print(request.POST)
            if 'Resolve' in request.POST:
                task_results.task_status = 'Closed'
            task_results.save()
            kanban_card_results = kanban_card.objects.filter(is_deleted='FALSE',
              task_id=task_id)
            for row in kanban_card_results:
                row.kanban_card_text = 'TASK' + str(task_id) + ' - ' + form.cleaned_data['task_short_description']
                row.save()

    initial = {'task_short_description':task_results.task_short_description,  'task_long_description':task_results.task_long_description, 
     'task_start_date':task_results.task_start_date, 
     'task_end_date':task_results.task_end_date}
    associated_project_results = project.objects.filter(is_deleted='FALSE',
      project_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id).values('project_id')))
    quote_results = quote.objects.filter(is_deleted='FALSE',
      task_id=task_results)
    requirement_results = requirement.objects.filter(is_deleted='FALSE',
      requirement_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id).values('requirement_id')))
    requirement_item_results = requirement_item.objects.filter(is_deleted='FALSE',
      requirement_item_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id).values('requirement_item_id')))
    running_total = 0
    t = loader.get_template('NearBeach/task_information.html')
    c = {'task_results':task_results, 
     'task_information_form':task_information_form(initial=initial), 
     'information_task_history_form':information_task_history_form(), 
     'associated_project_results':associated_project_results, 
     'media_url':settings.MEDIA_URL, 
     'task_id':task_id, 
     'permission':permission_results['task'], 
     'task_history_permissions':permission_results['task_history'], 
     'quote_results':quote_results, 
     'timezone':settings.TIME_ZONE, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'requirement_results':requirement_results, 
     'requirement_item_results':requirement_item_results, 
     'open_status':[
      'New', 'Open', 'Backlog']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def task_readonly(request, task_id):
    task_groups_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task.objects.get(task_id=task_id)).values('group_id_id')
    permission_results = return_user_permission_level(request, task_groups_results, ['task', 'task_history'])
    task_results = task.objects.get(task_id=task_id)
    to_do_results = to_do.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    task_history_results = task_history.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    email_results = email_content.objects.filter(is_deleted='FALSE',
      email_content_id__in=(email_contact.objects.filter(Q(task_id=task_id) & Q(is_deleted='FALSE') & Q(Q(is_private=False) | Q(change_user=(request.user)))).values('email_content_id')))
    requirement_results = requirement.objects.filter(is_deleted='FALSE',
      requirement_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id).values('requirement_id')))
    requirement_item_results = requirement_item.objects.filter(is_deleted='FALSE',
      requirement_item_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id).values('requirement_item_id')))
    associated_project_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    task_customers_results = task_customer.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    costs_results = cost.objects.filter(task_id=task_id,
      is_deleted='FALSE')
    quote_results = quote.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    bug_results = bug.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    assigned_results = object_assignment.objects.filter(task_id=task_id,
      is_deleted='FALSE').exclude(assigned_user=None).values('assigned_user__id', 'assigned_user', 'assigned_user__username', 'assigned_user__first_name', 'assigned_user__last_name').distinct()
    group_list_results = object_assignment.objects.filter(is_deleted='FALSE',
      task_id=task_id)
    task_history_collective = []
    for row in task_history_results:
        task_history_collective.append(task_history_readonly_form(initial={'task_history':row.task_history, 
         'submit_history':row.user_infomation + ' - ' + str(row.user_id) + ' - ' + row.date_created.strftime('%d %B %Y %H:%M.%S')},
          task_history_id=(row.task_history_id)))

    print(task_history_collective)
    t = loader.get_template('NearBeach/task_information/task_readonly.html')
    c = {'task_id':task_id, 
     'task_results':task_results, 
     'task_readonly_form':task_readonly_form(initial={'task_long_description': task_results.task_long_description}), 
     'to_do_results':to_do_results, 
     'task_history_collective':task_history_collective, 
     'email_results':email_results, 
     'associated_project_results':associated_project_results, 
     'task_customers_results':task_customers_results, 
     'costs_results':costs_results, 
     'quote_results':quote_results, 
     'bug_results':bug_results, 
     'assigned_results':assigned_results, 
     'group_list_results':group_list_results, 
     'project_permissions':permission_results['task'], 
     'project_history_permissions':permission_results['task_history'], 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'requirement_results':requirement_results, 
     'requirement_item_results':requirement_item_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def task_remove_customer(request, task_customer_id):
    if request.method == 'POST':
        task_customer_update = task_customer.objects.get(task_customer_id=task_customer_id)
        task_customer_update.change_user = request.user
        task_customer_update.is_deleted = 'TRUE'
        task_customer_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, can only do this in POST')


@login_required(login_url='login', redirect_field_name='')
def timeline(request):
    permission_results = return_user_permission_level(request, [], [])
    t = loader.get_template('NearBeach/timeline.html')
    c = {'timeline_form':timeline_form(), 
     'start_date':datetime.datetime.now(), 
     'end_date':datetime.datetime.now() + datetime.timedelta(days=31), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def timeline_data(request):
    if request.method == 'POST':
        form = timeline_form(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            object_type = form.cleaned_data['object_type']
            if object_type == 'Project':
                json_results = serializers.serialize('json',
                  (project.objects.filter(Q(is_deleted='FALSE') & Q(Q(project_start_date__lte=start_date, project_end_date__gte=end_date) | Q(project_start_date__gte=start_date, project_start_date__lte=end_date) | Q(project_end_date__gte=start_date,
                  project_end_date__lte=end_date))).order_by('project_start_date', 'project_end_date', 'project_id')),
                  fields={
                 'project_id',
                 'project_name',
                 'project_start_date',
                 'project_end_date',
                 'project_status'})
            else:
                if object_type == 'Task':
                    json_results = serializers.serialize('json',
                      (task.objects.filter(Q(is_deleted='FALSE') & Q(Q(task_start_date__lte=start_date, task_end_date__gte=end_date) | Q(task_start_date__gte=start_date, task_start_date__lte=end_date) | Q(task_end_date__gte=start_date,
                      task_end_date__lte=end_date))).order_by('task_start_date', 'task_end_date', 'task_id')),
                      fields={
                     'task_id',
                     'task_name',
                     'task_start_date',
                     'task_end_date',
                     'task_status'})
                else:
                    if object_type == 'Quote':
                        json_results = serializers.serialize('json',
                          (quote.objects.filter(is_deleted='FALSE',
                          quote_valid_till__gte=start_date,
                          quote_valid_till__lte=end_date).order_by('date_created', 'quote_valid_till', 'quote_id')),
                          fields={
                         'quote_id',
                         'quote_title',
                         'date_created',
                         'quote_valid_till',
                         'quote_stage'})
                        print(json_results)
                    else:
                        if object_type == 'Opportunity':
                            json_results = serializers.serialize('json',
                              (opportunity.objects.filter(is_deleted='FALSE',
                              opportunity_expected_close_date__gte=start_date,
                              opportunity_expected_close_date__lte=end_date).order_by('date_created', 'opportunity_expected_close_date', 'opportunity_id')),
                              fields={
                             'opportunity_id',
                             'opportunity_name',
                             'date_created',
                             'opportunity_expected_close_date',
                             'opportunity_stage_id',
                             'opportunity_stage'})
                        else:
                            return HttpResponseBadRequest('Sorry, there is no object that fits that situation')
            return HttpResponse(json_results, content_type='application/json')
        print(form.errors)
    else:
        return HttpResponseBadRequest('timeline date has to be done in post!')


@login_required(login_url='login', redirect_field_name='')
def timesheet_information(request, location_id, destination):
    if request.method == 'POST':
        form = new_timesheet_row(request.POST)
        if form.is_valid():
            timesheet_save = timesheet(timesheet_date=(form.cleaned_data['timesheet_date']),
              timesheet_start_time=(form.cleaned_data['timesheet_start_time']),
              timesheet_end_time=(form.cleaned_data['timesheet_end_time']),
              timesheet_description=(form.cleaned_data['timesheet_description']),
              change_user=(request.user))
            if destination == 'project':
                timesheet_save.project_id = location_id
            else:
                if destination == 'requirement_item':
                    timesheet_save.requirement_item_id = location_id
                else:
                    if destination == 'task':
                        timesheet_save.task_id = location_id
            timesheet_save.save()
        else:
            print(form.errors)
    elif destination == 'project':
        timesheet_results = timesheet.objects.filter(project_id=location_id)
    else:
        if destination == 'requirement_item':
            timesheet_results = timesheet.objects.filter(requirement_item=location_id)
        else:
            timesheet_results = timesheet.objects.filter(task_id=location_id)
    t = loader.get_template('NearBeach/timesheet/timesheet_information.html')
    c = {'new_timesheet_row':new_timesheet_row(), 
     'timesheet_results':timesheet_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def to_do_list(request, location_id, destination):
    if request.method == 'POST':
        form = to_do_form(request.POST)
        if form.is_valid():
            to_do_submit = to_do(to_do=(form.cleaned_data['to_do']),
              change_user=(request.user))
            if destination == 'project':
                to_do_submit.project = project.objects.get(project_id=location_id)
            else:
                if destination == 'task':
                    to_do_submit.task = task.objects.get(task_id=location_id)
                else:
                    to_do_submit.opportunity = opportunity.objects.get(opportunity_id=location_id)
            to_do_submit.save()
        else:
            print(form.errors)
    elif destination == 'project':
        to_do_results = to_do.objects.filter(is_deleted='FALSE',
          project_id=location_id)
    else:
        if destination == 'task':
            to_do_results = to_do.objects.filter(is_deleted='FALSE',
              task_id=location_id)
        else:
            to_do_results = to_do.objects.filter(is_deleted='FALSE',
              opportunity_id=location_id)
    t = loader.get_template('NearBeach/to_do/to_do.html')
    c = {'to_do_results':to_do_results, 
     'to_do_form':to_do_form()}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def to_do_complete(request, to_do_id):
    to_do_update = to_do.objects.get(to_do_id=to_do_id)
    to_do_update.to_do_completed = True
    to_do_update.save()
    t = loader.get_template('NearBeach/blank.html')
    c = {}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def user_want_remove(request, user_want_id):
    if request.method == 'POST':
        user_want_save = user_want.objects.get(pk=user_want_id)
        user_want_save.is_deleted = 'TRUE'
        user_want_save.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this function can only be done in POST')


@login_required(login_url='login', redirect_field_name='')
def user_want_view(request):
    if request.method == 'POST':
        form = user_want_form(request.POST)
        if form.is_valid():
            user_want_submit = user_want()
            user_want_submit.change_user = request.user
            user_want_submit.want_choice = form.cleaned_data['want_choice']
            user_want_submit.want_choice_text = form.cleaned_data['want_choice_text']
            user_want_submit.want_skill = form.cleaned_data['want_skill']
            user_want_submit.save()
        else:
            print(form.errors)
    want_results = user_want.objects.filter(is_deleted='FALSE',
      want_choice='1')
    not_want_results = user_want.objects.filter(is_deleted='FALSE',
      want_choice='0')
    t = loader.get_template('NearBeach/my_profile/user_want.html')
    c = {'user_want_form':user_want_form(), 
     'want_results':want_results, 
     'not_want_results':not_want_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def user_weblink_remove(request, user_weblink_id):
    if request.method == 'POST':
        weblink_save = user_weblink.objects.get(pk=user_weblink_id)
        weblink_save.is_deleted = 'TRUE'
        weblink_save.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Can only do this through post')


@login_required(login_url='login', redirect_field_name='')
def user_weblink_view(request):
    if request.method == 'POST':
        form = user_weblink_form(request.POST)
        if form.is_valid():
            user_weblink_submit = user_weblink(change_user=(request.user),
              user_weblink_url=(form.cleaned_data['user_weblink_url']),
              user_weblink_source=(form.cleaned_data['user_weblink_source']))
            user_weblink_submit.save()
        else:
            print(form.errors)
    user_weblink_results = user_weblink.objects.filter(is_deleted='FALSE',
      change_user=(request.user))
    t = loader.get_template('NearBeach/my_profile/user_weblink.html')
    c = {'user_weblink_form':user_weblink_form(), 
     'user_weblink_results':user_weblink_results}
    return HttpResponse(t.render(c, request))


def check_approval_status(rfc_id):
    """
    The following function will check the approval status of the RFC.

    Rules for Approval:
    - Any group with no group leaders are automatically approved. This is checked here
    - ALL groups must have approved the RFC
    :param rfc_id:
    :return:

    Method
    ~~~~~~
    1. Check for any auto approval groups
    2. Check to see if there are any waiting, cancelled, or rejected results
    3. If there are none then we approve the rfc
    """
    group_results = object_assignment.objects.filter(is_deleted='FALSE',
      request_for_change=rfc_id,
      group_id__isnull=False)
    for row in group_results:
        group_leader_count = user_group.objects.filter(is_deleted='FALSE',
          group_id=(row.group_id),
          group_leader=True).count()
        if group_leader_count == 0:
            request_for_change_group_approval.objects.filter(is_deleted='FALSE',
              rfc_id=rfc_id,
              group_id=(row.group_id),
              approval=1).update(approval=2)

    non_approve_count = request_for_change_group_approval.objects.filter(is_deleted='FALSE',
      rfc_id=rfc_id,
      approval__in=[
     1, 3, 4]).count()
    if non_approve_count == 0:
        rfc_results = request_for_change.objects.get(rfc_id=rfc_id)
        rfc_results.rfc_status = 3
        rfc_results.save()


def handler404(request):
    response = render('404.html',
      {}, context_instance=(RequestContext(request)))
    response.status_code = 404
    return response


def handler500(request):
    response = render('500.html',
      {}, context_instance=(RequestContext(request)))
    response.status_code = 500
    return response


def update_coordinates(campus_id):
    campus_results = campus.objects.get(pk=campus_id)
    address = campus_results.campus_address1 + ' ' + campus_results.campus_address2 + ' ' + campus_results.campus_address3 + ' ' + campus_results.campus_suburb + ' ' + campus_results.campus_region_id.region_name + ' ' + campus_results.campus_country_id.country_name + ' '
    print(address)
    address = address.replace('/', ' ')
    if hasattr(settings, 'GOOGLE_MAP_API_TOKEN'):
        print('Google Maps token exists')
        google_maps = GoogleMaps(api_key=(settings.GOOGLE_MAP_API_TOKEN))
        try:
            location = google_maps.search(location=address)
            first_location = location.first()
            campus_results.campus_longitude = first_location.lng
            campus_results.campus_latitude = first_location.lat
            campus_results.save()
        except:
            print('Sorry, there was an error getting the location details for this address.')

    else:
        if hasattr(settings, 'MAPBOX_API_TOKEN'):
            address_coded = urllib.parse.quote_plus(address)
            url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + address_coded + '.json?access_token=' + settings.MAPBOX_API_TOKEN
            if url.lower().startswith('http'):
                req = urllib.request.Request(url)
            else:
                raise ValueError from None
            with urllib.request.urlopen(req) as (response):
                data = json.load(response)
            try:
                campus_results.campus_longitude = data['features'][0]['center'][0]
                campus_results.campus_latitude = data['features'][0]['center'][1]
                campus_results.save()
                print(data['features'][0]['center'])
            except:
                print('No data for the address: ' + address)


def update_template_strings(variable, quote_results):
    """
    The following function will replace all {{ tag }} variables in the template with the results from the quote
    results. The current variables are;

    Groups
    ~~~~~~
    1.) Quotes
    2.) Organisatiions
    3.) Quote Billing Address
    """
    variable = variable.replace('{{ customer_id }}', str(quote_results.customer_id))
    variable = variable.replace('{{ customer_notes }}', quote_results.customer_notes)
    variable = variable.replace('{{ is_invoice }}', quote_results.is_invoice)
    variable = variable.replace('{{ opportunity_id }}', str(quote_results.opportunity_id))
    variable = variable.replace('{{ organisation_id }}', str(quote_results.organisation_id))
    variable = variable.replace('{{ project_id }}', str(quote_results.project_id))
    variable = variable.replace('{{ quote_billing_address }}', str(quote_results.quote_billing_address))
    variable = variable.replace('{{ quote_id }}', str(quote_results.quote_id))
    variable = variable.replace('{{ quote_stage_id }}', str(quote_results.quote_stage_id))
    variable = variable.replace('{{ quote_terms }}', quote_results.quote_terms)
    variable = variable.replace('{{ quote_title }}', quote_results.quote_title)
    variable = variable.replace('{{ quote_valid_till }}', str(quote_results.quote_valid_till))
    variable = variable.replace('{{ task_id }}', str(quote_results.task_id))
    if quote_results.organisation_id:
        variable = variable.replace('{{ organisation_name }}', quote_results.organisation_id.organisation_name)
        variable = variable.replace('{{ organisation_website }}', quote_results.organisation_id.organisation_website)
        variable = variable.replace('{{ organisation_email }}', quote_results.organisation_id.organisation_email)
    else:
        variable = variable.replace('{{ organisation_name }}', '')
        variable = variable.replace('{{ organisation_website }}', '')
        variable = variable.replace('{{ organisation_email }}', '')
    if quote_results.quote_billing_address:
        variable = variable.replace('{{ billing_address1 }}', quote_results.quote_billing_address.campus_address1)
        variable = variable.replace('{{ billing_address2 }}', quote_results.quote_billing_address.campus_address2)
        variable = variable.replace('{{ billing_address3 }}', quote_results.quote_billing_address.campus_address3)
        variable = variable.replace('{{ campus_id }}', str(quote_results.quote_billing_address.campus_id))
        variable = variable.replace('{{ campus_nickname }}', quote_results.quote_billing_address.campus_nickname)
        variable = variable.replace('{{ campus_phone }}', quote_results.quote_billing_address.campus_phone)
        variable = variable.replace('{{ campus_region_id }}', str(quote_results.quote_billing_address.campus_region_id))
        variable = variable.replace('{{ billing_suburb }}', quote_results.quote_billing_address.campus_suburb)
        if quote_results.quote_billing_address.campus_postcode == None:
            variable = variable.replace('{{ billing_postcode }}', '')
        else:
            variable = variable.replace('{{ billing_postcode }}', str(quote_results.quote_billing_address.campus_postcode))
        variable = variable.replace('{{ billing_region }}', str(quote_results.quote_billing_address.campus_region_id))
        variable = variable.replace('{{ billing_country }}', str(quote_results.quote_billing_address.campus_country_id))
    else:
        variable = variable.replace('{{ billing_address1 }}', '')
        variable = variable.replace('{{ billing_address2 }}', '')
        variable = variable.replace('{{ billing_address3 }}', '')
        variable = variable.replace('{{ billing_postcode }}', '')
        variable = variable.replace('{{ campus_id }}', '')
        variable = variable.replace('{{ campus_nickname }}', '')
        variable = variable.replace('{{ campus_phone }}', '')
        variable = variable.replace('{{ campus_region_id }}', '')
        variable = variable.replace('{{ billing_suburb }}', '')
        variable = variable.replace('{{ billing_region }}', '')
        variable = variable.replace('{{ billing_country }}', '')
    return variable