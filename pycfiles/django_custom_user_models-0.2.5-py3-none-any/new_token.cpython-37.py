# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\views\jwt\new_token.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 561 bytes
from django.http import HttpRequest, JsonResponse
from CustomAuth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def new_jwt_token(request: HttpRequest):
    """
    If user logged in return user jwt token that expire after 2 month
    :param request: Client request
    :return: A json response that contains jwt-authentication
    """
    user = request.user
    token = user.token
    response = {'jwt-authentication': token}
    return JsonResponse(response, status=200)