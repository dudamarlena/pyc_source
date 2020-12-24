# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\workspace\django-template-project\source\apps\web\views.py
# Compiled at: 2011-06-19 15:52:36
"""
Common web-app views
"""
from django.views.generic.base import TemplateView

class Greetings(TemplateView):
    template_name = 'web/base.html'


greetings = Greetings.as_view()