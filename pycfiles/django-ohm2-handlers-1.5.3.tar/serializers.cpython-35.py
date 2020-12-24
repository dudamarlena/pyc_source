# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/currencies/serializers.py
# Compiled at: 2016-12-06 14:21:50
# Size of source mod 2**32: 296 bytes
from django.contrib.auth.models import User as AuthUser
from rest_framework import serializers
from . import models
from . import settings