# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/urls.py
# Compiled at: 2017-06-13 10:26:46
# Size of source mod 2**32: 354 bytes
from django.conf.urls import url, include
from rest_framework import routers
from ovp_uploads import views
router = routers.DefaultRouter()
router.register('uploads/images', views.UploadedImageViewSet, 'upload-images')
router.register('image-gallery', views.ImageGalleryViewSet, 'image-gallery')
urlpatterns = [
 url('^', include(router.urls))]