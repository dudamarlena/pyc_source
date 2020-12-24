# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-statistic/vkontakte_groups_statistic/views.py
# Compiled at: 2013-08-08 08:23:08
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import VkontakteDeniedAccessError, Group, parse_statistic_for_group
from forms import GroupImportStatisticForm
import re, logging
log = logging.getLogger('vkontakte_groups_statistic')

def import_statistic(request, redirect_url_name=None, form_class=GroupImportStatisticForm):
    context = {'message': ''}
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            try:
                group = form.save()
                if redirect_url_name:
                    try:
                        return HttpResponseRedirect(reverse(redirect_url_name, args=('vk', group.id)))
                    except:
                        context['message'] = 'Статистика группы импортирована успешно'

            except VkontakteDeniedAccessError:
                context['message'] = 'Вы не имеете доступа к статистике группы'

    else:
        form = form_class()
    context['form'] = form
    return render_to_response('vkontakte_groups_statistic/import_group_statistic.html', context, context_instance=RequestContext(request))


@csrf_exempt
def import_statistic_via_bookmarklet(request, redirect_url_name=None, redirect_kwargs=None):
    try:
        url, content = request.POST['url'], request.POST['body']
    except KeyError:
        return HttpResponseRedirect('/')

    m = re.findall('http://vk.com/stats\\?(?:act=([^&]+)&)?gid=(\\d+)/?', url)
    if len(m) == 0:
        log.error('Url of vkontakte group statistic should be started with http://vk.com/stats?gid=')
        return HttpResponseRedirect('/')
    else:
        act, group_id = m[0]
        group = Group.remote.fetch(ids=[group_id])[0]
        parse_statistic_for_group(group, act, content)
        if redirect_kwargs is None:
            redirect_kwargs = {}
        redirect_kwargs['object_id'] = group.id
        try:
            return HttpResponseRedirect(reverse(redirect_url_name, kwargs=redirect_kwargs))
        except:
            return HttpResponseRedirect('/')

        return