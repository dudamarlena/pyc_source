# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/views/view.py
# Compiled at: 2018-07-30 04:21:32
# Size of source mod 2**32: 965 bytes
import uuid
from django.core.exceptions import ImproperlyConfigured
from django.views import generic
from django.forms import models as model_forms
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
import workon.views, workon.utils
__all__ = [
 'View', 'ModalView']

class View(generic.DetailView):

    def get_template_names(self):
        if self.request.is_ajax():
            return getattr(self, 'ajax_template_name', getattr(self, 'template_name_ajax', getattr(self, 'xhr_template_name', getattr(self, 'template_name_xhr', getattr(self, 'template_name')))))
        else:
            return self.template_name


class ModalView(View):
    pass