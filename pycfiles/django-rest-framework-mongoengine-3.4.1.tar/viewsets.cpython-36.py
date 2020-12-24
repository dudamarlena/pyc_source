# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: w:\projects\django-rest-framework-mongoengine\rest_framework_mongoengine\viewsets.py
# Compiled at: 2019-09-19 16:31:31
# Size of source mod 2**32: 776 bytes
from rest_framework import mixins
from rest_framework.viewsets import ViewSetMixin
from rest_framework_mongoengine.generics import GenericAPIView

class GenericViewSet(ViewSetMixin, GenericAPIView):
    __doc__ = ' Adaptation of DRF GenericViewSet '


class ModelViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    __doc__ = ' Adaptation of DRF ModelViewSet '


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    __doc__ = ' Adaptation of DRF ReadOnlyModelViewSet '