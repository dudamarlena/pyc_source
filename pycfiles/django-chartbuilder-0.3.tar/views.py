# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andy/dev/chartbuilder/django_chartbuilder/views.py
# Compiled at: 2014-05-25 00:06:23
from django.shortcuts import render

def home(request):
    return render(request, 'django_chartbuilder/chartbuilder.html')