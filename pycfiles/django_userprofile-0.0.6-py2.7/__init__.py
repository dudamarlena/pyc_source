# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/userprofile/__init__.py
# Compiled at: 2012-05-29 05:24:39
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from userprofile import utils
user_profile_module = getattr(settings, 'USER_PROFILE_MODULE', None)
if not user_profile_module:
    raise ImproperlyConfigured('You must provide an USER_PROFILE_MODULE setting.')
profile_model = utils.get_profile_model()
User.profile = property(lambda u: profile_model.objects.get_or_create(user=u)[0])