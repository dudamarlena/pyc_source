# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\works\py\ipdiranproject\django-role-permissions\rolepermissions\__init__.py
# Compiled at: 2018-12-21 08:06:44
# Size of source mod 2**32: 401 bytes
import django
from distutils.version import StrictVersion
__version__ = '2.2.1rc1'
try:
    dj_version = StrictVersion(django.get_version())
except:
    dj_version = StrictVersion('1.10')

if dj_version < StrictVersion('1.7'):
    from rolepermissions.loader import load_roles_and_permissions
    load_roles_and_permissions()
else:
    default_app_config = 'rolepermissions.apps.RolePermissions'