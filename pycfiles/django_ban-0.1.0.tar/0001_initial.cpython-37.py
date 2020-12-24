# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\Desktop\programlarim\djangoapps\django_ban\django_ban\migrations\0001_initial.py
# Compiled at: 2019-07-26 09:51:28
# Size of source mod 2**32: 2994 bytes
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('djangoip', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Config',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'permission_request_count', models.IntegerField(default=6, help_text='Permission request count')),
      (
       'remove_ban_time', models.IntegerField(default=60, help_text='After how many second, ban removed')),
      (
       'permission_second', models.IntegerField(default=1, help_text="IP ne kadar süre de 'permission_request_count' sayısı kadar istek atabilir."))],
       options={'abstract': False}),
     migrations.CreateModel(name='IPBan',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'start', models.DateTimeField(default=(django.utils.timezone.now), verbose_name='Saved time')),
      (
       'count', models.IntegerField(default=1, verbose_name='Requests count')),
      (
       'ban', models.BooleanField(default=0)),
      (
       'ip', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djangoip.IpModel', verbose_name='IP'))],
       options={'verbose_name': 'Ip'}),
     migrations.CreateModel(name='Url',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'permission_request_count', models.IntegerField(default=6, help_text='Permission request count')),
      (
       'remove_ban_time', models.IntegerField(default=60, help_text='After how many second, ban removed')),
      (
       'permission_second', models.IntegerField(default=1, help_text="IP ne kadar süre de 'permission_request_count' sayısı kadar istek atabilir.")),
      (
       'url_pattern', models.CharField(max_length=600)),
      (
       'url_name', models.CharField(max_length=200)),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created'))],
       options={'verbose_name': 'Url'}),
     migrations.AlterUniqueTogether(name='url',
       unique_together={
      ('url_pattern', 'url_name')}),
     migrations.AddField(model_name='ipban',
       name='url',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='django_ban.Url'))]