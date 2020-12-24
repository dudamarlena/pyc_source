# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/urls.py
# Compiled at: 2018-02-05 14:41:56
# Size of source mod 2**32: 476 bytes
from django.urls import path
from . import views
app_name = 'um'
urlpatterns = [
 path('settings/account', (views.AccountSettings.as_view()), name='settings-account'),
 path('settings/interface', (views.InterfaceSettings.as_view()), name='settings-interface'),
 path('settings/email', (views.EmailSettings.as_view()), name='settings-email'),
 path('settings/security', (views.SecuritySettings.as_view()), name='settings-security')]