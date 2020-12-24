# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: w:\projects\django-rest-framework-mongoengine\rest_framework_mongoengine\generics.py
# Compiled at: 2019-09-19 16:31:31
# Size of source mod 2**32: 4518 bytes
from django.http import Http404
from mongoengine import DoesNotExist, ValidationError
from mongoengine.queryset.base import BaseQuerySet
from rest_framework import generics as drf_generics
from rest_framework import mixins

def get_object_or_404(queryset, *args, **kwargs):
    """ replacement of rest_framework.generics and django.shrtcuts analogues """
    try:
        return (queryset.get)(*args, **kwargs)
    except (ValueError, TypeError, DoesNotExist, ValidationError):
        raise Http404()


class GenericAPIView(drf_generics.GenericAPIView):
    __doc__ = ' Adaptation of DRF GenericAPIView '
    lookup_field = 'id'

    def get_queryset(self):
        queryset = super(GenericAPIView, self).get_queryset()
        if isinstance(queryset, BaseQuerySet):
            queryset = queryset.all()
        return queryset

    def get_object(self):
        """"""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, 'Expected view %s to be called with a URL keyword argument named "%s". Fix your URL conf, or set the `.lookup_field` attribute on the view correctly.' % (
         self.__class__.__name__, lookup_url_kwarg)
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class CreateAPIView(mixins.CreateModelMixin, GenericAPIView):
    __doc__ = 'Adaptation of DRF CreateAPIView'

    def post(self, request, *args, **kwargs):
        return (self.create)(request, *args, **kwargs)


class ListAPIView(mixins.ListModelMixin, GenericAPIView):
    __doc__ = 'Adaptation of DRF ListAPIView'

    def get(self, request, *args, **kwargs):
        return (self.list)(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    __doc__ = 'Adaptation of DRF ListCreateAPIView'

    def get(self, request, *args, **kwargs):
        return (self.list)(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return (self.create)(request, *args, **kwargs)


class RetrieveAPIView(mixins.RetrieveModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return (self.retrieve)(request, *args, **kwargs)


class UpdateAPIView(mixins.UpdateModelMixin, GenericAPIView):
    __doc__ = 'Adaptation of DRF UpdateAPIView'

    def put(self, request, *args, **kwargs):
        return (self.update)(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return (self.partial_update)(request, *args, **kwargs)


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    __doc__ = 'Adaptation of DRF RetrieveUpdateAPIView'

    def get(self, request, *args, **kwargs):
        return (self.retrieve)(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return (self.update)(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return (self.partial_update)(request, *args, **kwargs)


class RetrieveDestroyAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    __doc__ = 'Adaptation of DRF RetrieveDestroyAPIView'

    def get(self, request, *args, **kwargs):
        return (self.retrieve)(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return (self.destroy)(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    __doc__ = 'Adaptation of DRF RetrieveUpdateDestroyAPIView'

    def get(self, request, *args, **kwargs):
        return (self.retrieve)(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return (self.update)(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return (self.partial_update)(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return (self.destroy)(request, *args, **kwargs)