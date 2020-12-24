# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0049_auto_20191226_1809.py
# Compiled at: 2019-12-26 05:09:42
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0048_auto_20191226_1413')]
    operations = [
     migrations.AlterField(model_name=b'campaignrecord', name=b'bind_preuser', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_crm.PreUser', verbose_name=b'红包发放新peruser账号'))]