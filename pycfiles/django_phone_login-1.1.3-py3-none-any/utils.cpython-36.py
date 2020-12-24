# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ray/Work/Rumor/django-phone-login/phone_login/utils.py
# Compiled at: 2017-08-01 15:46:19
# Size of source mod 2**32: 1367 bytes
from rest_framework import status
from rest_framework.authtoken.models import Token
STATUS = {'status':None, 
 'message':None}

def too_many_requests():
    STATUS['status'] = status.HTTP_429_TOO_MANY_REQUESTS
    STATUS['message'] = 'Reached max limit for the day.'
    return (STATUS, STATUS['status'])


def unauthorized():
    STATUS['status'] = status.HTTP_401_UNAUTHORIZED
    STATUS['message'] = 'User not logged in.'
    return (STATUS, STATUS['status'])


def failure(message='Failed'):
    STATUS['status'] = status.HTTP_400_BAD_REQUEST
    STATUS['message'] = message
    return (STATUS, STATUS['status'])


def success(message=None):
    STATUS['status'] = status.HTTP_200_OK
    STATUS['message'] = message
    return (STATUS, STATUS['status'])


def user_detail(user, last_login):
    try:
        token = user.auth_token.key
    except:
        token = Token.objects.create(user=user)
        token = token.key

    user_json = {'id':user.pk,  'last_login':last_login, 
     'token':token, 
     'status':status.HTTP_200_OK}
    return user_json


def model_field_attr(model, model_field, attr):
    """
    Returns the specified attribute for the specified field on the model class.
    """
    fields = dict([(field.name, field) for field in model._meta.fields])
    return getattr(fields[model_field], attr)