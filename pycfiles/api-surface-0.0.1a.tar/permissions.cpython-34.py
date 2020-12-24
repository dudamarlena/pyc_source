# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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