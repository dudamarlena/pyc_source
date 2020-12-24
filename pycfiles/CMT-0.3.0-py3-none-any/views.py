# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cms_test_app\views.py
# Compiled at: 2019-06-25 04:07:41
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect
import json, pytz, requests, ast

def home(request):
    user = request.user
    args = {'user': user}
    return render(request, 'alerts/home.html', args)