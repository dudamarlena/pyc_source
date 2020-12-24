# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/views/terms/terms.py
# Compiled at: 2019-10-28 01:58:06
# Size of source mod 2**32: 886 bytes
from __future__ import unicode_literals
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils
from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsDeveloper
from irekua_rest_api.permissions import ReadOnly

class TermViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, utils.CustomViewSetMixin, GenericViewSet):
    queryset = models.Term.objects.all()
    serializer_mapping = utils.SerializerMapping.from_module(serializers.terms.terms)
    permission_mapping = utils.PermissionMapping(default=(IsDeveloper | IsAdmin | ReadOnly))