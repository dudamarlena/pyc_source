# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mikhail/.virtualenvs/django-robokassa/lib/python3.5/site-packages/robokassa/views.py
# Compiled at: 2018-04-26 07:03:25
# Size of source mod 2**32: 3811 bytes
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from robokassa.conf import USE_POST
from robokassa.forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
from robokassa.models import SuccessNotification
from robokassa.signals import result_received, success_page_visited, fail_page_visited

@csrf_exempt
def receive_result(request):
    """Обработчик для ResultURL."""
    data = request.POST if USE_POST else request.GET
    form = ResultURLForm(data)
    if form.is_valid():
        inv_id, out_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']
        notification = SuccessNotification.objects.create(InvId=inv_id, OutSum=out_sum)
        result_received.send(sender=notification, InvId=inv_id, OutSum=out_sum, extra=form.extra_params())
        return HttpResponse('OK%s' % inv_id)
    return HttpResponse('error: bad signature')


@csrf_exempt
def success(request, template_name='robokassa/success.html', extra_context=None, error_template_name='robokassa/error.html'):
    """Обработчик для SuccessURL"""
    data = request.POST if USE_POST else request.GET
    form = SuccessRedirectForm(data)
    if form.is_valid():
        inv_id, out_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']
        success_page_visited.send(sender=form, InvId=inv_id, OutSum=out_sum, extra=form.extra_params())
        context = {'InvId': inv_id, 'OutSum': out_sum, 'form': form}
        context.update(form.extra_params())
        context.update(extra_context or {})
        return TemplateResponse(request, template_name, context)
    return TemplateResponse(request, error_template_name, {'form': form})


@csrf_exempt
def fail(request, template_name='robokassa/fail.html', extra_context=None, error_template_name='robokassa/error.html'):
    """Обработчик для FailURL"""
    data = request.POST if USE_POST else request.GET
    form = FailRedirectForm(data)
    if form.is_valid():
        inv_id, out_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']
        fail_page_visited.send(sender=form, InvId=inv_id, OutSum=out_sum, extra=form.extra_params())
        context = {'InvId': inv_id, 'OutSum': out_sum, 'form': form}
        context.update(form.extra_params())
        context.update(extra_context or {})
        return TemplateResponse(request, template_name, context)
    return TemplateResponse(request, error_template_name, {'form': form})