# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0003_auto_20181205_2108.py
# Compiled at: 2018-12-05 08:08:57
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_message', '0002_auto_20181205_2103')]
    operations = [
     migrations.AlterField(model_name=b'sendrecord', name=b'to_user', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_message_to_user', to=settings.AUTH_USER_MODEL, verbose_name=b'发送给'))]