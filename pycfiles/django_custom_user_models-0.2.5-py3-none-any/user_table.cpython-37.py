# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\tables\user_table.py
# Compiled at: 2020-01-27 19:20:15
# Size of source mod 2**32: 305 bytes
import django_tables2 as tables
from CustomAuth.models import User

class UserTable(tables.Table):

    class Meta:
        model = User
        template_name = 'django_tables2/bootstrap.html'
        fields = ('email', 'full_name', 'is_verify', 'is_staff', 'is_superuser', 'jalali_last_login')