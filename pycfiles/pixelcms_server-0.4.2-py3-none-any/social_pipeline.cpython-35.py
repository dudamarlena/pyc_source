# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/accounts/social_pipeline.py
# Compiled at: 2017-01-12 08:30:36
# Size of source mod 2**32: 668 bytes
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthException

class EmailIsTaken(AuthException):

    def __str__(self):
        return _('Email address associated with this account is already taken.')


def is_email_taken(backend, uid, user=None, social=None, *args, **kwargs):
    email = kwargs['details'].get('email')
    try:
        existing_user = get_user_model().objects.get(email=email)
        if existing_user == user:
            return
        raise EmailIsTaken(backend)
    except get_user_model().DoesNotExist:
        return