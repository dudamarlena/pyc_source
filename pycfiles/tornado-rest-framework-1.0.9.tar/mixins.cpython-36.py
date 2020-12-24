# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/views/mixins.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 4395 bytes
from rest_framework import serializers
from rest_framework.core.exceptions import SkipFilterError
from rest_framework.lib.orm.query import AsyncEmptyQuery
from rest_framework.utils import status
__all__ = [
 'CreateModelMixin',
 'ListModelMixin',
 'RetrieveModelMixin',
 'UpdateModelMixin',
 'DestroyModelMixin']

class CreateModelMixin:
    __doc__ = '\n    创建\n    '

    async def perform_create(self, form):
        """
        :param form:
        :return:
        """
        instance = await form.save()
        return instance

    async def create(self, *args, **kwargs):
        form = self.get_form()
        if await form.is_valid():
            instance = await self.perform_create(form)
            if self.need_obj_serializer:
                self.create_serializer(form)
                serializer = self.get_serializer(instance=instance)
                result = await serializer.data
            else:
                pk = instance._meta.primary_key.name
                result = {'{}'.format(pk): getattr(instance, pk, None)}
            return self.write_response(data=result, status_code=(status.HTTP_201_CREATED))
        else:
            return self.write_response(data=(await form.errors), status_code=(status.HTTP_400_BAD_REQUEST))

    def create_serializer(self, form):
        """
        如果没有定义self.serializer_class，则自动创建
        :param form:
        :return:
        """
        if self.serializer_class is not None:
            return

        class Serializer(serializers.ModelSerializer):

            class Meta:
                model = form.Meta.model
                fields = '__all__'

        self.serializer_class = Serializer


class ListModelMixin:
    __doc__ = '\n    分页查询列表\n    '

    async def list(self, *args, **kwargs):
        try:
            queryset = await self.filter_queryset(self.get_queryset())
        except SkipFilterError:
            queryset = AsyncEmptyQuery()

        page = await self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return await self.write_paginated_response(await serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return self.write_response(await serializer.data)


class RetrieveModelMixin:
    __doc__ = '\n    查看详情\n    '

    async def retrieve(self, *args, **kwargs):
        instance = await self.get_object()
        serializer = self.get_serializer(instance=instance)
        return self.write_response(await serializer.data)


class UpdateModelMixin:
    __doc__ = '\n    修改实例对象\n    '

    async def update(self, *args, **kwargs):
        obj_instance = await self.get_object()
        form = self.get_form(empty_permitted=True, instance=obj_instance)
        if await form.is_valid():
            instance = await self.perform_update(form)
            if self.need_obj_serializer:
                self.create_serializer(form)
                serializer = self.get_serializer(instance=instance)
                result = await serializer.data
            else:
                pk = instance._meta.primary_key.name
                result = {'{}'.format(pk): getattr(instance, pk, None)}
            return self.write_response(data=result, status_code=(status.HTTP_200_OK))
        else:
            return self.write_response(data=(await form.errors), status_code=(status.HTTP_400_BAD_REQUEST))

    async def perform_update(self, form):
        instance = await form.save()
        return instance

    def create_serializer(self, form):
        """
        如果没有定义self.serializer_class，则自动创建
        :param form:
        :return:
        """
        if self.serializer_class is not None:
            return

        class Serializer(serializers.ModelSerializer):

            class Meta:
                model = form.Meta.model
                fields = '__all__'

        self.serializer_class = Serializer


class DestroyModelMixin:
    __doc__ = '\n    删除对象\n    '

    async def destroy(self, *args, **kwargs):
        instance = await self.get_object()
        del_rows = await self.perform_destroy(instance)
        return self.write_response(data=dict(rows=del_rows), status_code=(status.HTTP_200_OK))

    async def perform_destroy(self, instance):
        del_rows = await instance.delete_instance()
        return del_rows