# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\users\ma_k\appdata\local\temp\pip-build-s8wja0\httplog\httplog\views.py
# Compiled at: 2016-11-28 21:21:16
from rest_framework import viewsets
from .filters import HttpLogFilter
from .serializers import HttpLogSerializer
from .models.httplog import HttpLog

class HttpLogViewSet(viewsets.ModelViewSet):
    queryset = HttpLog.objects.all().order_by('id')
    serializer_class = HttpLogSerializer
    filter_class = HttpLogFilter