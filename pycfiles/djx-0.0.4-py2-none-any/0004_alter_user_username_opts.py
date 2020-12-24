# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/auth/migrations/0004_alter_user_username_opts.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
from django.contrib.auth import validators
from django.db import migrations, models
from django.utils import six

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0003_alter_user_email_max_length')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'username', field=models.CharField(error_messages={b'unique': b'A user with that username already exists.'}, max_length=30, validators=[
      validators.UnicodeUsernameValidator() if six.PY3 else validators.ASCIIUsernameValidator()], help_text=b'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name=b'username'))]