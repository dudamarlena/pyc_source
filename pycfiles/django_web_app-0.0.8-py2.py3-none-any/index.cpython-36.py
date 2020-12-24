# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\work\work\PycharmProjects\UpcwangyingWebApp\web_app\views\index.py
# Compiled at: 2018-08-01 08:31:50
# Size of source mod 2**32: 187 bytes
from django.shortcuts import render
from django.views.generic import View

class IndexView(View):

    def get(self, request):
        return render(request, 'web_app/index.html')