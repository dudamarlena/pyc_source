# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variant/admin.py
# Compiled at: 2014-08-25 20:19:38
from django.contrib import admin
from .models import Experiment
admin.site.register(Experiment)