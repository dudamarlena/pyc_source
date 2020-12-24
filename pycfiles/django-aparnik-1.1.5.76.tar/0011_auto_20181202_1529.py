# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0011_auto_20181202_1529.py
# Compiled at: 2018-12-03 11:15:34
from __future__ import unicode_literals
from django.db import migrations

def negative_default_value(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    User = apps.get_model(b'aparnik_users', b'User')
    User.objects.filter(limit_device_login=0).update(limit_device_login=-1)
    User.objects.filter(co_sale_percentage_value=0).update(co_sale_percentage_value=-1)


def zero_default_value(apps, schema_editor):
    User = apps.get_model(b'aparnik_users', b'User')
    User.objects.filter(limit_device_login=-1).update(limit_device_login=0)
    User.objects.filter(co_sale_percentage_value=-1).update(co_sale_percentage_value=0)


class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0010_auto_20181202_1528')]
    operations = [
     migrations.RunPython(negative_default_value, reverse_code=zero_default_value)]