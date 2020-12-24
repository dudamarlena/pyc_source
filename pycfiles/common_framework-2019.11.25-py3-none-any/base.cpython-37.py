# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/api/base.py
# Compiled at: 2018-10-19 05:01:41
# Size of source mod 2**32: 2459 bytes
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
try:
    from rest_framework.authtoken.models import Token
    assert 'rest_framework.authtoken' in settings.INSTALLED_APPS
except (AssertionError, ImportError):
    Token = None

from common.api.permissions import CurrentUserPermissions
from common.api.serializers import UserSerializer
from common.api.utils import create_api, disable_relation_fields
from common.api.viewsets import UserViewSet
from common.models import MODELS, MetaData, GroupMetaData, UserMetaData
User = get_user_model()
SERIALIZERS = {}
VIEWSETS = {}
SERIALIZERS_BASE = {User: (UserSerializer,), 
 Group: (), 
 UserMetaData: (), 
 GroupMetaData: (), 
 Permission: (), 
 ContentType: (), 
 LogEntry: (), 
 Token: ()}
VIEWSETS_BASE = {User: (UserViewSet,)}
SERIALIZERS_DATA = {}
VIEWSETS_DATA = {}
QUERYSETS = {}
METADATA = {}
CONFIGS = {MetaData: dict(depth=0), 
 Group: dict(many_to_many=True, depth=1, permissions=[CurrentUserPermissions]), 
 GroupMetaData: dict(permissions=[CurrentUserPermissions]), 
 User: dict(many_to_many=True, depth=1, permissions=[CurrentUserPermissions]), 
 UserMetaData: dict(permissions=[CurrentUserPermissions])}
DEFAULT_CONFIG = dict(depth=1)
CurrentUserPermissions.filters.update({User: lambda request: dict(id=(request.user.pk)), 
 Group: lambda request: dict(user=(request.user)), 
 UserMetaData: lambda request: dict(user=(request.user)), 
 GroupMetaData: lambda request: dict(group__user=(request.user))})
disable_relation_fields(User, Group, Permission, ContentType, LogEntry, Token, *MODELS)
router, *_ = create_api(User, Group, Permission, ContentType, LogEntry, Token, *MODELS)