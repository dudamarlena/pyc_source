# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/views.py
# Compiled at: 2017-04-26 15:46:47
# Size of source mod 2**32: 1242 bytes
from ovp_testimonials import models
from ovp_testimonials import helpers
from ovp_testimonials import serializers
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions

class TestimonialResource(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    __doc__ = '\n  TestimonialResource endpoint\n  '
    queryset = models.Testimonial.objects.filter(published=True)

    def create(self, request, *args, **kwargs):
        if not helpers.get_settings().get('CAN_CREATE_TESTIMONIAL_UNAUTHENTICATED', False):
            request.data['user'] = request.user.pk
        return super(TestimonialResource, self).create(request, *args, **kwargs)

    def get_permissions(self):
        request = self.get_serializer_context()['request']
        if self.action == 'create':
            if helpers.get_settings().get('CAN_CREATE_TESTIMONIAL_UNAUTHENTICATED', False):
                self.permission_classes = ()
        else:
            self.permission_classes = (
             permissions.IsAuthenticated,)
        return super(TestimonialResource, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.TestimonialCreateSerializer
        return serializers.TestimonialRetrieveSerializer