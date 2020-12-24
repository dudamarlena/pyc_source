# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jeff/Development/python/g_recaptcha/g_recaptcha/validate_recaptcha.py
# Compiled at: 2016-09-08 04:34:27
from django.http import HttpResponse
from django.conf import settings
import urllib, urllib2, json
from django.shortcuts import render

def validate_captcha(view):
    """
    Decorator to validate a captcha, settings from django

    @validate_Captcha
    def a_view():
        ...
    """

    def wrap(request, *args, **kwargs):

        def failure_http():
            return render(request, 'captcha_fail.html', status=401)

        def failure_ajax():
            return HttpResponse('There was a problem with the captcha, please try again', status=401)

        if request.method == 'POST':
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY, 
               'response': request.POST.get('g-recaptcha-response', None), 
               'remoteip': request.META.get('REMOTE_ADDR', None)}
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.loads(response.read())
            if result['success']:
                return view(request, *args, **kwargs)
            if request.is_ajax():
                return failure_ajax()
            return failure_http()
        return view(request, *args, **kwargs)

    wrap._original = view
    return wrap