# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\urls\handler.py
# Compiled at: 2019-12-12 12:55:52
# Size of source mod 2**32: 278 bytes
from django.urls import path
from CustomAuth.views import page_not_found, permission_denied, server_error, unauthorized, bad_request
handler400 = bad_request
handler401 = unauthorized
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error