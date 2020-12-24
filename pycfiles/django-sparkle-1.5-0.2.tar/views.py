# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/spielmann/prog/bitchest/server/env/src/django-sparkle/sparkle/views.py
# Compiled at: 2013-07-23 04:00:31
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.models import Site
from django.utils import timezone
from sparkle.models import Application, Version, SystemProfileReport, SystemProfileReportRecord

def appcast(request, application_slug):
    """Generate the appcast for the given application while recording any system profile reports"""
    application = get_object_or_404(Application, slug=application_slug)
    if len(request.GET):
        report = SystemProfileReport.objects.create(ip_address=request.META.get('REMOTE_ADDR'))
        for key, value in request.GET.iteritems():
            record = SystemProfileReportRecord.objects.create(report=report, key=key, value=value)

    return render(request, 'sparkle/appcast.xml', {'application': application})