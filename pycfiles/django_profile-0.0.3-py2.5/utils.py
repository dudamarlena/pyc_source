# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/profile/utils.py
# Compiled at: 2010-08-04 04:05:50
from django.conf import settings

def get_profile_model():
    """
    Returns configured user profile model or None if not found
    """
    auth_profile_module = getattr(settings, 'AUTH_PROFILE_MODULE', None)
    profile_model = None
    if auth_profile_module:
        (app_label, model) = auth_profile_module.split('.')
        profile_model = getattr(__import__('%s.models' % app_label, globals(), locals(), [model], -1), model, None)
    return profile_model