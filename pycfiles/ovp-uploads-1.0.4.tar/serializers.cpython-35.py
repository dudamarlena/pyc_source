# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/serializers.py
# Compiled at: 2017-06-13 10:27:08
# Size of source mod 2**32: 2169 bytes
from django.conf import settings
from ovp_uploads.models import UploadedImage
from rest_framework import serializers
if hasattr(settings, 'GCS_BUCKET'):
    GCS_BASE_URI = str.join('/', ('https://storage.googleapis.com', settings.GCS_BUCKET))

    def build_absolute_uri(req, image):
        return image.url


else:

    def build_absolute_uri(req, image):
        if image:
            return req.build_absolute_uri(image.url)


class UploadedImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_small_url = serializers.SerializerMethodField()
    image_medium_url = serializers.SerializerMethodField()
    image_large_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedImage
        fields = ('id', 'user', 'image', 'image_url', 'image_small_url', 'image_medium_url',
                  'image_large_url')
        read_only_fields = ('image_small', 'image_medium', 'image_large')
        extra_kwargs = {'image': {'write_only': True}, 'crop_rect': {'write_only': True}}

    def get_image_url(self, obj):
        return build_absolute_uri(self.context['request'], obj.image)

    def get_image_small_url(self, obj):
        return build_absolute_uri(self.context['request'], obj.image_small)

    def get_image_medium_url(self, obj):
        return build_absolute_uri(self.context['request'], obj.image_medium)

    def get_image_large_url(self, obj):
        return build_absolute_uri(self.context['request'], obj.image_large)


class ImageGallerySerializer(UploadedImageSerializer):
    name = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)

    class Meta:
        model = UploadedImage
        read_only_fields = ('image_small', 'image_medium', 'image_large')
        fields = ('id', 'image_url', 'image_small_url', 'image_medium_url', 'image_large_url',
                  'name', 'category')