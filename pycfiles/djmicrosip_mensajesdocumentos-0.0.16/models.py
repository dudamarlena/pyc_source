# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_mensajesdocumentos\djmicrosip_mensajesdocumentos\models.py
# Compiled at: 2015-09-04 12:49:48
from django.db import models
from django_microsip_base.libs.models_base.models import Almacen, Registry
from django.conf import settings
if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
    from djmicrosip_tareas.models import ProgrammedTask
    from djmicrosip_tareas.models import PendingTask