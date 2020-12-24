# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/django_common/lib/python2.7/site-packages/django_common/auth_backends.py
# Compiled at: 2012-03-11 19:20:35
import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        """
        "username" being passed is really email address and being compared to as such.
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            logging.warn('Unsuccessful login attempt using username/email: %s' % username)

        return