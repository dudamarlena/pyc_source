# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/urls.py
# Compiled at: 2020-04-03 12:47:55
# Size of source mod 2**32: 313 bytes
from django.urls import path, include
from . import views
urlpatterns = [
 path('phone-number/sent/', views.PhoneNumberView.as_view()),
 path('resend/<int:phonenumber_id>/confirmation/', views.ResendConfirmationView.as_view()),
 path('phone-number/confirmation/', views.PINConfirmationView.as_view())]