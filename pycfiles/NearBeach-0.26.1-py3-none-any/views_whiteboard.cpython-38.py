# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/views_whiteboard.py
# Compiled at: 2020-05-09 19:50:11
# Size of source mod 2**32: 6672 bytes
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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.template import loader
from NearBeach.forms import *
from .models import *
from django.db.models import Q
from .misc_functions import *
from .user_permissions import return_user_permission_level
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def whiteboard_common_xml(request):
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_common.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_graph_xml(request):
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_graph.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_editor_xml(request):
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_editor.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_information(request, whiteboard_id):
    """
    Whiteboard information
    ~~~~~~~~~~~~~~~~~~~~~~
    Permission: We need to get the groups connected to the whiteboard. For example if the whiteboard is connected to a
    task - we need to get that task's group ID.
    :param request:
    :return:
    """
    document_results = document.objects.get(is_deleted='FALSE',
      whiteboard_id=whiteboard_id)
    document_permission_results = document_permission.objects.filter(is_deleted='FALSE',
      document_key=document_results)
    whiteboard_group_results = object_assignment.objects.filter(Q(is_deleted='FALSE') & Q(Q(task_id__in=(document_permission_results.filter(task_id__isnull=False).values('task_id'))) | Q(project_id__in=(document_permission_results.filter(project_id__isnull=False).values('project_id'))) | Q(requirement_id__in=(document_permission_results.filter(requirement_id__isnull=False).values('requirement_id'))) | Q(request_for_change__in=(document_permission_results.filter(request_for_change__isnull=False).values('request_for_change'))) | Q(opportunity_id__in=(document_permission_results.filter(opportunity_id__isnull=False).values('opportunity_id'))))).values('group_id')
    permission_results = return_user_permission_level(request, whiteboard_group_results, [
     'project',
     'task',
     'requirement',
     'request_for_change',
     'opportunity',
     'customer',
     'organisation'])
    bypass_permissions = len(object_assignment.objects.filter(Q(is_deleted='FALSE',
      whiteboard_id=whiteboard_id) & Q(Q(customer_id__isnull=False) | Q(organisation_id__isnull=False))))
    if bypass_permissions == 0:
        if permission_results['project'] == 0:
            if permission_results['task'] == 0:
                if permission_results['requirement'] == 0:
                    if permission_results['request_for_change'] == 0:
                        if permission_results['opportunity'] == 0:
                            return HttpResponseRedirect(reverse('permission_denied'))
    whiteboard_results = get_object_or_404(whiteboard, whiteboard_id=whiteboard_id)
    t = loader.get_template('NearBeach/whiteboard/whiteboard_information.html')
    c = {'whiteboard_results':whiteboard_results, 
     'whiteboard_id':whiteboard_id, 
     'permission_results':permission_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def whiteboard_save(request, whiteboard_id):
    if request.method == 'POST':
        whiteboard_update = whiteboard.objects.get(whiteboard_id=whiteboard_id)
        whiteboard_update.whiteboard_xml = request.POST['whiteboard_xml']
        whiteboard_update.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, this function only requests POST')


@login_required(login_url='login')
def whiteboard_toolbar_xml(request):
    print('Made contact with Whiteboard POST :)')
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_toolbar.xml')
    c = {}
    return HttpResponse((t.render(c, request)), content_type='application/xhtml+xml')