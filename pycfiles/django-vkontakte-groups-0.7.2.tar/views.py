# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-groups/vkontakte_groups/views.py
# Compiled at: 2015-01-25 02:59:50
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from vkontakte_groups_statistic.models import GroupStat, GroupStatPercentage, VkontakteDeniedAccessError
from models import Group
from forms import GroupImportStatisticForm, GroupImportPostsForm
import re, logging

def import_posts(request, redirect_url_name=None, form_class=GroupImportPostsForm):
    context = {'message': ''}
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            group = form.save()
            if redirect_url_name:
                try:
                    return HttpResponseRedirect(reverse(redirect_url_name, args=('vk', group.id)))
                except:
                    context['message'] = 'Сообщения группы импортированы успешно'

    else:
        form = form_class()
    context['form'] = form
    return render_to_response('vkontakte_groups/import_group_posts.html', context, context_instance=RequestContext(request))