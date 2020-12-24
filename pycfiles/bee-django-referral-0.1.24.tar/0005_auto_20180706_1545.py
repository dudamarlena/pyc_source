# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0005_auto_20180706_1545.py
# Compiled at: 2018-07-06 03:45:20
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_referral', '0004_auto_20180515_1557')]
    operations = [
     migrations.CreateModel(name=b'UserActivity', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID'))], options={b'db_table': b'bee_django_referral_user_activity'}),
     migrations.AddField(model_name=b'activity', name=b'show_type', field=models.IntegerField(choices=[(1, '全部显示'), (2, '部分显示')], default=1, verbose_name=b'显示类型')),
     migrations.AddField(model_name=b'useractivity', name=b'activity', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_referral.Activity')),
     migrations.AddField(model_name=b'useractivity', name=b'user', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]