# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyzima-spb/www-python/django-adminlte-full/demo/adminlte_full/views.py
# Compiled at: 2016-06-19 07:40:19
# Size of source mod 2**32: 1697 bytes
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

class BaseView(TemplateView):
    _BaseView__instance = None

    @classmethod
    def replace_with(cls, instance):
        cls._BaseView__instance = instance

    @classmethod
    def instance(cls):
        return cls._BaseView__instance or cls


class MessageView(BaseView):
    template_name = 'adminlte_full/base-layout.html'

    def get(self, request, *args, **kwargs):
        messages.debug(request, 'Redefine this page')
        return render(request, self.template_name)


class NotificationView(BaseView):
    template_name = 'adminlte_full/base-layout.html'

    def get(self, request, *args, **kwargs):
        messages.debug(request, 'Redefine this page')
        return render(request, self.template_name)


class TaskView(BaseView):
    template_name = 'adminlte_full/base-layout.html'

    def get(self, request, *args, **kwargs):
        messages.debug(request, 'Redefine this page')
        return render(request, self.template_name)


def index(request):
    pass


@login_required
def password_change_done(request, template_name='registration/password_change_done.html', extra_context=None):
    messages.success(request, _('Password change successful'))