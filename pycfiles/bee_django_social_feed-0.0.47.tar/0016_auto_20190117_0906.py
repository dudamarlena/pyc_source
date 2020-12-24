# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0016_auto_20190117_0906.py
# Compiled at: 2019-01-16 20:06:54
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_social_feed', '0015_auto_20181018_0834')]
    operations = [
     migrations.AddField(model_name=b'feed', name=b'is_star', field=models.BooleanField(default=False, verbose_name=b'是否精华')),
     migrations.AddField(model_name=b'feed', name=b'star_at', field=models.DateTimeField(blank=True, null=True, verbose_name=b'加精时间')),
     migrations.AddField(model_name=b'feed', name=b'star_by', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'star_operator', to=settings.AUTH_USER_MODEL, verbose_name=b'由谁加精'))]