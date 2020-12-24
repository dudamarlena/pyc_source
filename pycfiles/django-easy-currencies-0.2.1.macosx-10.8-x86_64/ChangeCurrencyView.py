# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/views/ChangeCurrencyView.py
# Compiled at: 2014-10-16 04:19:59
from __future__ import unicode_literals
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic.base import View

class ChangeCurrencyView(View):

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        """
        Sets currency in session then redirects to the previous page.

        :param request:
        :param args:
        :param kwargs:
        :return: :rtype:
        """
        request.session[b'currency'] = request.POST.get(b'currency', b'USD')
        origin = self.request.META.get(b'HTTP_REFERER', b'/')
        return HttpResponseRedirect(origin)