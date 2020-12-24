# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pauloostenrijk/WebProjects/django-user-verification/verification/urls.py
# Compiled at: 2016-05-16 16:32:02
# Size of source mod 2**32: 653 bytes
from rest_framework import routers
from django.conf.urls import url
from .views import VerificationRedirectorView, SendVerificationAPIView
urlpatterns = [
 url('^verify/send/(?P<verification_type>[0-9A-Za-z_\\-]+)/$', SendVerificationAPIView.as_view(), name='verification-send'),
 url('^verify/(?P<verification_type>[0-9A-Za-z_\\-]+)/(?P<code>[^/.]+)/$', VerificationRedirectorView.as_view(template_name='verification/redirector.html'), name='verification-redirector')]
router = routers.DefaultRouter(trailing_slash=False)
urlpatterns += router.urls