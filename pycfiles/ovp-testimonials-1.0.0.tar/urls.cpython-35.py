# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-testimonials/ovp_testimonials/urls.py
# Compiled at: 2017-04-26 14:57:23
# Size of source mod 2**32: 306 bytes
from django.conf.urls import url, include
from rest_framework import routers
from ovp_testimonials import views
testimonials = routers.SimpleRouter()
testimonials.register('testimonials', views.TestimonialResource, 'testimonial')
urlpatterns = [
 url('^testimonials/', include(testimonials.urls))]