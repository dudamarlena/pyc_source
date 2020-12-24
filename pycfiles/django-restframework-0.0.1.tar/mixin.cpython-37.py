# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/django_rest_framework/django_restframework/mixins/mixin.py
# Compiled at: 2019-04-23 01:35:43
# Size of source mod 2**32: 4416 bytes
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from django_restframework.serializers.serializer import SerializerPlug
from django_restframework.paginations.pagination import MyPagination
from rest_framework.views import APIView

class MyCreateModeMixin(CreateModelMixin, GenericViewSet, SerializerPlug):
    authentication_classes = ()
    permission_classes = ()
    msg_create = '创建成功'
    results_display = True

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=(request.data))
        self.validation_error(serializer=serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data if self.results_display else None
        return Response({'success':True, 
         'msg':self.msg_create, 
         'results':data},
          status=(status.HTTP_200_OK))


class MyDeleteModelMixin(DestroyModelMixin, GenericViewSet):
    authentication_classes = ()
    permission_classes = ()
    msg_delete = '成功删除'
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success':True, 
         'msg':self.msg_delete, 
         'results':None},
          status=(status.HTTP_204_NO_CONTENT))


class MyUpdateModelMixin(UpdateModelMixin, GenericViewSet, SerializerPlug):
    authentication_classes = ()
    permission_classes = ()
    msg_update = '修改成功'
    lookup_field = 'pk'
    results_display = True

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=(request.data), partial=partial)
        self.validation_error(serializer=serializer)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        data = serializer.data if self.results_display else None
        return Response({'success':True, 
         'msg':self.msg_update, 
         'results':data},
          status=(status.HTTP_200_OK))


class MyListModeMixin(ListModelMixin, GenericViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = MyPagination
    msg_list = '成功获取列表数据'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success':True, 
         'msg':self.msg_list, 
         'results':serializer.data},
          status=(status.HTTP_200_OK))


class MyRetrieveModelMixin(RetrieveModelMixin, GenericViewSet):
    authentication_classes = ()
    permission_classes = ()
    msg_detail = '成功获取详细数据'
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'success':True, 
         'msg':self.msg_detail, 
         'results':serializer.data},
          status=(status.HTTP_200_OK))


class MyAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()