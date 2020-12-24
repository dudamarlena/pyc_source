# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/views.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 1264 bytes
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http.response import JsonResponse
from django.utils.html import strip_tags
from aparnik.contrib.basemodels.models import BaseModel

def install(request):
    context = {'title': 'نصب'}
    template_name = 'aparnik/index.html'
    return render(request, template_name=template_name, context=context)


def share(request):
    pk = request.GET.get('id', 0)
    ref = request.GET.get('ref', '')
    model = get_object_or_404((BaseModel.objects.all()), pk=pk).get_real_instance()
    title = strip_tags(model.get_title())
    description = strip_tags(model.get_description())
    context = {'title':title, 
     'description':description, 
     'app_url':request.build_absolute_uri(model.get_api_uri()), 
     'install_app_url':request.build_absolute_uri(reverse('aparnik:install')), 
     'model':model}
    template_name = 'aparnik/share.html'
    return render(request, template_name=template_name, context=context)