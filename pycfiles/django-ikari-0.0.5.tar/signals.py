# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zenobius/Dev/django-apps/django-ikari/ikari/signals.py
# Compiled at: 2013-08-01 23:54:43
import logging
from django.dispatch import Signal
from . import settings
logger = logging.getLogger(__name__)
logger.addHandler(settings.null_handler)
domain_request = Signal()