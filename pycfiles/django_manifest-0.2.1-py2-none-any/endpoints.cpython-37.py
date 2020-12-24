# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/dev_reactor/django-reactor/manifest/endpoints.py
# Compiled at: 2019-10-15 15:31:41
# Size of source mod 2**32: 2667 bytes
""" Manifest REST API URLs
"""
from django.conf.urls import url
from manifest import api_views
from manifest.messages import REGION_UPDATE_SUCCESS
from manifest.serializers import ProfileUpdateSerializer, RegionUpdateSerializer
urlpatterns = [
 url('^login/$',
   (api_views.AuthLoginAPIView.as_view()),
   name='auth_login_api'),
 url('^logout/$', (api_views.AuthLogoutAPIView.as_view()),
   name='auth_logout_api'),
 url('^register/$', (api_views.AuthRegisterAPIView.as_view()),
   name='auth_register_api'),
 url('^activate/$', (api_views.AuthActivateAPIView.as_view()),
   name='auth_activate_api'),
 url('^password/reset/$', (api_views.PasswordResetAPIView.as_view()),
   name='password_reset_api'),
 url('^password/reset/verify/$', (api_views.PasswordResetVerifyAPIView.as_view()),
   name='password_reset_verify_api'),
 url('^password/reset/confirm/$', (api_views.PasswordResetConfirmAPIView.as_view()),
   name='password_reset_confirm_api'),
 url('^profile/$', (api_views.AuthProfileAPIView.as_view()),
   name='auth_profile_api'),
 url('^profile/options/$', api_views.ProfileOptionsAPIView.as_view(serializer_class=ProfileUpdateSerializer),
   name='profile_options_api'),
 url('^profile/update/$', api_views.AuthProfileAPIView.as_view(serializer_class=ProfileUpdateSerializer),
   name='profile_update_api'),
 url('^profile/update/region/$', api_views.AuthProfileAPIView.as_view(serializer_class=RegionUpdateSerializer,
   success_message=REGION_UPDATE_SUCCESS),
   name='region_update_api'),
 url('^picture/upload/$', (api_views.PictureUploadAPIView.as_view()),
   name='picture_upload_api'),
 url('^email/change/$', (api_views.EmailChangeAPIView.as_view()),
   name='email_change_api'),
 url('^email/change/confirm/$', (api_views.EmailChangeConfirmAPIView.as_view()),
   name='email_change_confirm_api'),
 url('^password/change/$', (api_views.PasswordChangeAPIView.as_view()),
   name='password_change_api'),
 url('^users/$', (api_views.UserListAPIView.as_view()),
   name='user_list_api'),
 url('^users/(?P<username>\\w+)/$', (api_views.UserDetailAPIView.as_view()),
   name='user_detail_api')]