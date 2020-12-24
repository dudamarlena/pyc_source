# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0017_feedcomment_to_user.py
# Compiled at: 2019-01-25 19:42:19
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_social_feed', '0016_auto_20190117_0906')]
    operations = [
     migrations.AddField(model_name=b'feedcomment', name=b'to_user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'to_user', to=settings.AUTH_USER_MODEL))]