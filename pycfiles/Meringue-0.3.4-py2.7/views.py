# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/views.py
# Compiled at: 2015-08-22 16:34:49
from django.http import HttpResponse

def im_a_teapot(request):
    return HttpResponse(status=418)