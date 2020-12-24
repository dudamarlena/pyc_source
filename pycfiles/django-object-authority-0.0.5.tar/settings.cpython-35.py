# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/settings.py
# Compiled at: 2017-06-09 06:50:44
# Size of source mod 2**32: 1222 bytes
"""
Settings for Django object authority are all namespaced in the OBJECT_AUTHORITY setting.
For example your project's `settings.py` file might look like this:

OBJECT_AUTHORITY_AUTHORIZE_BY_DEFAULT = True
OBJECT_AUTHORITY_FULL_PERMISSION_FOR_STAFF = True
OBJECT_AUTHORITY_FULL_PERMISSION_FOR_SUPERUSERS = True
"""
from django.conf import settings
AUTHORIZE_BY_DEFAULT = getattr(settings, 'OBJECT_AUTHORITY_AUTHORIZE_BY_DEFAULT', True)
FULL_PERMISSION_FOR_STAFF = getattr(settings, 'OBJECT_AUTHORITY_FULL_PERMISSION_FOR_STAFF', False)
FULL_PERMISSION_FOR_SUPERUSERS = getattr(settings, 'OBJECT_AUTHORITY_FULL_PERMISSION_FOR_SUPERUSERS', True)
CHECK_PERMISSION_CLASS_BY_DEFAULT = getattr(settings, 'OBJECT_AUTHORITY_CHECK_PERMISSION_CLASS_BY_DEFAULT', True)
PERMISSION_FOR_MODELS = getattr(settings, 'OBJECT_AUTHORITY_PERMISSION_FOR_MODELS', None)
PERMISSION_FOR_APPLICATIONS = getattr(settings, 'OBJECT_AUTHORITY_PERMISSION_FOR_APPLICATIONS', None)
DEFAULT_PERMISSIONS = ('view', 'add', 'change', 'delete')