# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/emails/migrations/0002_massmessage.py
# Compiled at: 2017-01-10 18:14:18
# Size of source mod 2**32: 1432 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('emails', '0001_initial')]
    operations = [
     migrations.CreateModel(name='MassMessage', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'subject', models.CharField(max_length=255, verbose_name='subject')),
      (
       'content', models.TextField(verbose_name='content')),
      (
       'reply_to', models.CharField(max_length=255, verbose_name='reply to')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'sent', models.BooleanField(default=False, verbose_name='sent')),
      (
       'postdate', models.DateTimeField(blank=True, null=True, verbose_name='postdate')),
      (
       'recipients', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='recipients'))], options={'verbose_name': 'mass message', 
      'ordering': ('-created', ), 
      'verbose_name_plural': 'mass messages'})]