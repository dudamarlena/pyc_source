# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/serializers.py
# Compiled at: 2017-04-26 15:46:20
# Size of source mod 2**32: 567 bytes
from ovp_testimonials import models
from ovp_users.serializers import ShortUserPublicRetrieveSerializer
from rest_framework import serializers

class TestimonialCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Testimonial
        fields = ['content', 'rating', 'user', 'created_date']
        read_only_fields = ['created_date']


class TestimonialRetrieveSerializer(serializers.ModelSerializer):
    user = ShortUserPublicRetrieveSerializer

    class Meta:
        model = models.Testimonial
        fields = ['content', 'rating', 'user', 'created_date']