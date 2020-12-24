# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thomas/Dev/Project/django-trusts/trusts/__init__.py
# Compiled at: 2016-04-16 22:35:57
from __future__ import unicode_literals
from django.conf import settings
from django.apps import apps as django_apps
ENTITY_MODEL_NAME = getattr(settings, b'TRUSTS_ENTITY_MODEL', getattr(settings, b'AUTH_USER_MODEL', b'auth.User'))
GROUP_MODEL_NAME = getattr(settings, b'TRUSTS_GROUP_MODEL', b'auth.Group')
PERMISSION_MODEL_NAME = getattr(settings, b'TRUSTS_PERMISSION_MODEL', b'auth.Permission')
DEFAULT_SETTLOR = getattr(settings, b'TRUSTS_DEFAULT_SETTLOR', None)
ALLOW_NULL_SETTLOR = getattr(settings, b'TRUSTS_ALLOW_NULL_SETTLOR', DEFAULT_SETTLOR == None)
ROOT_PK = getattr(settings, b'TRUSTS_ROOT_PK', 1)

def get_entity_model():
    """
    Returns the Entity model. By default it is
    """
    try:
        return django_apps.get_model(ENTITY_MODEL_NAME)
    except ValueError:
        raise ImproperlyConfigured(b"TRUSTS_ENTITY_MODEL or AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(b"TRUSTS_ENTITY_MODEL or AUTH_USER_MODEL refers to model '%s' that has not been installed" % ENTITY_MODEL_NAME)


def get_group_model():
    """
    Returns the Group model
    """
    try:
        return django_apps.get_model(GROUP_MODEL)
    except ValueError:
        raise ImproperlyConfigured(b"TRUSTS_GROUP_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(b"TRUSTS_GROUP_MODEL refers to model '%s' that has not been installed" % GROUP_MODEL_NAME)


def get_permission_model():
    """
    Returns the Group model
    """
    try:
        return django_apps.get_model(PERMISSION_MODEL_NAME)
    except ValueError:
        raise ImproperlyConfigured(b"TRUSTS_PERMISSION_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(b"TRUSTS_PERMISSION_MODEL refers to model '%s' that has not been installed" % PERMISSION_MODEL_NAME)


default_app_config = b'trusts.apps.AppConfig'