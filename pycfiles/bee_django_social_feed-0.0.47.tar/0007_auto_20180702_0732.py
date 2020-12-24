# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0007_auto_20180702_0732.py
# Compiled at: 2018-07-01 19:32:20
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_social_feed', '0006_auto_20180701_0938')]
    operations = [
     migrations.CreateModel(name=b'Album', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'note', models.TextField(verbose_name=b'感受')),
      (
       b'created_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'updated_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at']}),
     migrations.RemoveField(model_name=b'albumphoto', name=b'user'),
     migrations.AddField(model_name=b'albumphoto', name=b'album', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_social_feed.Album'))]