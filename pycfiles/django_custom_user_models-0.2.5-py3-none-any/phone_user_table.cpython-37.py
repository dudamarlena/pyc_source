# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\tables\phone_user_table.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 347 bytes
from django_tables2 import tables
from CustomAuth.models import PhoneNumberUser

class PhoneUserTable(tables.Table):

    class Meta:
        model = PhoneNumberUser
        template_name = 'django_tables2/bootstrap.html'
        fields = ('full_name', 'cellphone', 'email', 'is_verify', 'is_staff', 'is_superuser',
                  'jalali_last_login')