# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/workspaces/workspace_django/django-celerybeat-status/celerybeat_status/views.py
# Compiled at: 2018-02-15 23:46:56
# Size of source mod 2**32: 1104 bytes
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from celerybeat_status.helpers import get_periodic_tasks_info

class PeriodicTasksStatusListView(TemplateView):
    template_name = 'celerybeat_status/periodic_tasks_status_list.html'
    site_url = '/'

    @method_decorator(user_passes_test(lambda u: u.is_staff and u.is_superuser, login_url='admin:login'))
    def dispatch(self, request, *args, **kwargs):
        return super(PeriodicTasksStatusListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PeriodicTasksStatusListView, self).get_context_data(**kwargs)
        context['title'] = _('Periodic tasks status')
        context['user'] = self.request.user
        context['site_url'] = self.site_url
        context['has_permission'] = self.request.user.is_superuser
        context['tasks'] = get_periodic_tasks_info()
        return context