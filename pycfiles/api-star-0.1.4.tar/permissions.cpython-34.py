# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/permissions.py
# Compiled at: 2016-04-14 15:42:18
# Size of source mod 2**32: 471 bytes


def is_authenticated():

    def has_permission(request):
        return bool(request.auth)

    return has_permission


def is_authenticated_or_read_only():

    def has_permission(request):
        return bool(request.auth) or request.method in ('GET', 'HEAD', 'OPTIONS')

    return has_permission