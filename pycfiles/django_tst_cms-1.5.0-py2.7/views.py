# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\django_tst_cms\views.py
# Compiled at: 2019-06-25 04:07:41
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect
import json, pytz, requests, ast

def home(request):
    user = request.user
    args = {'user': user}
    return render(request, 'alerts/home.html', args)