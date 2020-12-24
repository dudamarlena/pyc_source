# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/settings.py
# Compiled at: 2018-10-10 10:40:36
# Size of source mod 2**32: 1061 bytes
import django.conf as user_settings
from common.utils import singleton

@singleton
class Settings:
    """Settings"""
    default = dict(SERVICE_USAGE=False,
      SERVICE_USAGE_DEFAULT={},
      SERVICE_USAGE_DATA={},
      SERVICE_USAGE_LIMIT_ONLY=False,
      IGNORE_LOG=False,
      IGNORE_GLOBAL=False,
      NOTIFY_CHANGES=False,
      NOTIFY_OPTIONS={},
      WEBSOCKET_ENABLED=False,
      WEBSOCKET_URL='',
      FRONTEND_SECRET_KEY='',
      LDAP_ENABLE=False,
      LDAP_LOGIN='',
      LDAP_HOST='',
      LDAP_BASE='',
      LDAP_FILTER='',
      LDAP_ATTRIBUTES=[],
      LDAP_ADMIN_USERS=[],
      LDAP_STAFF_USERS=[],
      LDAP_ADMIN_GROUPS=[],
      LDAP_STAFF_GROUPS=[],
      LDAP_GROUP_PREFIX='')

    def __getattr__(self, item):
        return getattr(user_settings, item, self.default.get(item, None))


settings = Settings()