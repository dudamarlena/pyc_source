# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/permissions.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 953 bytes
from explorer import app_settings
from explorer.utils import allowed_query_pks, user_can_see_query

def view_permission(request, **kwargs):
    return app_settings.EXPLORER_PERMISSION_VIEW(request.user) or user_can_see_query(request, **kwargs) or app_settings.EXPLORER_TOKEN_AUTH_ENABLED() and (request.META.get('HTTP_X_API_TOKEN') == app_settings.EXPLORER_TOKEN or request.GET.get('token') == app_settings.EXPLORER_TOKEN)


def view_permission_list(request):
    return app_settings.EXPLORER_PERMISSION_VIEW(request.user) or allowed_query_pks(request.user.id)


def change_permission(request, *args, **kwargs):
    return app_settings.EXPLORER_PERMISSION_CHANGE(request.user)