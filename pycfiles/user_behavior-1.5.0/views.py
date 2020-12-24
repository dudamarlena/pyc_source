# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/views.py
# Compiled at: 2016-11-17 22:38:22
from rest_framework import viewsets
from .filters import ApiInfoFilter, UserBehaviorFilter
from .serializers import ApiInfoSerializer, UserBehaviorSerializer
from .models.api_info import ApiInfo
from .models.user_behavior import UserBehavior

class ApiInfoViewSet(viewsets.ModelViewSet):
    queryset = ApiInfo.objects.all().order_by('id')
    serializer_class = ApiInfoSerializer
    filter_class = ApiInfoFilter


class UserBehaviorViewSet(viewsets.ModelViewSet):
    queryset = UserBehavior.objects.all()
    serializer_class = UserBehaviorSerializer
    filter_class = UserBehaviorFilter