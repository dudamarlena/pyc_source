# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/profile/__init__.py
# Compiled at: 2010-08-04 04:05:50
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from profile import utils
auth_profile_module = getattr(settings, 'AUTH_PROFILE_MODULE', None)
if not auth_profile_module:
    raise ImproperlyConfigured('You must provide an AUTH_PROFILE_MODULE setting.')
profile_model = utils.get_profile_model()
User.profile = property(lambda u: profile_model.objects.get_or_create(user=u)[0])