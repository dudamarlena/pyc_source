# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0013_unique_user_label.py
# Compiled at: 2020-02-24 10:26:32
# Size of source mod 2**32: 763 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('django_fido', '0012_authenticator_label')]
    operations = [
     migrations.AlterField(model_name='authenticator',
       name='label',
       field=models.TextField(blank=True, default='', max_length=255),
       preserve_default=False),
     migrations.AlterUniqueTogether(name='authenticator',
       unique_together=(set([('user', 'label')])))]