# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/userprofile/utils.py
# Compiled at: 2012-05-29 05:24:39
from django.conf import settings
from django.db.models.loading import get_model

def get_profile_model():
    """
    Returns configured user profile model or None if not found
    """
    user_profile_module = getattr(settings, 'USER_PROFILE_MODULE', None)
    if user_profile_module:
        app_label, model_name = user_profile_module.split('.')
        return get_model(app_label, model_name)
    else:
        return
        return