# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/__init__.py
# Compiled at: 2017-06-09 06:51:17
# Size of source mod 2**32: 806 bytes
from .authorizations import authorization, NoAuthorizationRegistered, AlreadyAuthorizationRegistered
from .decorators import register
from .filters import AuthorityBaseFilter, BaseFilter
from .loader import autodiscover_authorizations
from .mixins import AuthorizationMixin
from .options import BaseObjectAuthorization, BaseUserObjectAuthorization
__version__ = '0.0.5'
default_app_config = 'django_object_authority.apps.DjangoObjectAuthorityConfig'
__all__ = [
 'AuthorityBaseFilter', 'AlreadyAuthorizationRegistered', 'AuthorizationMixin', 'BaseFilter',
 'BaseObjectAuthorization', 'BaseUserObjectAuthorization', 'NoAuthorizationRegistered', 'authorization',
 'autodiscover', 'register']

def autodiscover():
    autodiscover_authorizations('authorizations', register_to=authorization)