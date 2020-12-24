# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/views.py
# Compiled at: 2020-04-15 06:20:40
# Size of source mod 2**32: 991 bytes
from __future__ import annotations
from typing import TYPE_CHECKING
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormView
from .forms import SampleForm
if TYPE_CHECKING:
    from django.http import HttpRequest

def cleaned_data_check(data: 'dict') -> 'None':
    """ Function that doesn't do anythingbut is mocked by integration tests to check if cleaned_data is right """
    pass


class SampleFormView(FormView):
    template_name = 'integration.html'
    form_class = SampleForm
    success_url = '/integration/submit'

    def form_valid(self, form):
        cleaned_data_check(form.cleaned_data)
        return super().form_valid(form)


class DownloadView(View):

    def post(self, request: 'HTTPRequest') -> 'HttpResponse':
        response = HttpResponse('content of example.txt', content_type='plain/text')
        response['Content-Disposition'] = 'inline; filename=example.txt'
        return response