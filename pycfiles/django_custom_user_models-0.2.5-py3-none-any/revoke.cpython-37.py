# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\views\jwt\revoke.py
# Compiled at: 2019-12-21 08:37:14
# Size of source mod 2**32: 353 bytes
from django.http import HttpRequest, JsonResponse
from CustomAuth.models import User
from CustomAuth.decorators import jwt_required

@jwt_required
def revoke(request: HttpRequest):
    user = request.user
    token = user.token
    response = {'jwt-authentication': token}
    return JsonResponse(response, status=200)