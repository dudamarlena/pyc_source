# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tony/work/buser/djamail/djamail/views.py
# Compiled at: 2019-10-14 23:30:26
# Size of source mod 2**32: 106 bytes
from django.shortcuts import render

def preview(request):
    return render(request, 'preview.html', {})