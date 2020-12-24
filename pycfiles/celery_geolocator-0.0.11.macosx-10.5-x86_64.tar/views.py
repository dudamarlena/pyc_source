# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brent/anaconda/envs/fba/lib/python2.7/site-packages/examples/django_celery/demoapp/views.py
# Compiled at: 2014-08-09 13:41:56
from django.shortcuts import render
from demoapp.tasks import xsum

def sum_task(request, a, b):
    promise = xsum.delay([a, b])
    result = promise.get()
    return render(request, 'demoapp/sum.html', {'a': a, 
       'b': b, 
       'result': result})