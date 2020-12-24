# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seraf/Cycloid/Cyclosible/cyclosible/appversion/views.py
# Compiled at: 2015-12-22 05:07:25
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from .models import AppVersion
from .serializers import AppVersionSerializer

class AppVersionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows interact with applications versions.
    """
    queryset = AppVersion.objects.all()
    serializer_class = AppVersionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('env', 'playbook', 'application', 'version', 'deployed')
    permission_classes = (permissions.IsAuthenticated,)