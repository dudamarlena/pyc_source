# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0017_auto_20190428_0959.py
# Compiled at: 2019-04-28 08:07:10
from __future__ import unicode_literals
from django.db import migrations
import random, string

def randomPassword():
    """Generate a random password """
    randomSource = string.ascii_letters + string.digits
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    for i in range(155):
        password += random.choice(randomSource)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = (b'').join(passwordList)
    return password


def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model(b'settings', b'Setting')
    key = b''
    try:
        key = b'SECRET_KEY'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'کلید امنیتی تبادل اطلاعات', key=key, value=randomPassword(), value_type=b's', is_show=True, is_variable_in_home=False)

    try:
        key = b'ORDER_SYNC_WITH_WEBSITES'
        Setting.objects.get(key=key)
    except Exception:
        Setting.objects.create(title=b'ای پی آی سینک شدن فاکتور ها با وبسایت', key=key, value=b'', value_type=b's', is_show=False, is_variable_in_home=False)


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Setting = apps.get_model(b'settings', b'Setting')
    try:
        key = b'SECRET_KEY'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass

    try:
        key = b'ORDER_SYNC_WITH_WEBSITES'
        Setting.objects.get(key=key).delete()
    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0016_auto_20190204_1825')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]