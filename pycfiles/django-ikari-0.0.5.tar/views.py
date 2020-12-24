# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zenobius/Dev/django-apps/django-ikari/ikari/views.py
# Compiled at: 2013-08-01 23:57:28
import logging
from django.views.generic import TemplateView
from . import settings
logger = logging.getLogger(__name__)
logger.addHandler(settings.null_handler)

class DomainErrorView(TemplateView):
    template_name = 'domains/error.html'