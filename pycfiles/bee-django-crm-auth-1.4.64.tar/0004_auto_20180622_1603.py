# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0004_auto_20180622_1603.py
# Compiled at: 2018-06-26 00:36:23
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_crm', '0003_auto_20180608_1917')]
    operations = [
     migrations.AddField(model_name=b'preuser', name=b'referral_user1', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_crm_referral_user1', to=settings.AUTH_USER_MODEL, verbose_name=b'推荐人')),
     migrations.AddField(model_name=b'preuser', name=b'referral_user2', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_crm_referral_user2', to=settings.AUTH_USER_MODEL, verbose_name=b'接引人')),
     migrations.AlterField(model_name=b'preuser', name=b'referral_user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_crm_referral_user', to=settings.AUTH_USER_MODEL, verbose_name=b'原推荐人'))]