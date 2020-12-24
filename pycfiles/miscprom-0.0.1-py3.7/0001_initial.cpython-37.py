# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/wanikani/migrations/0001_initial.py
# Compiled at: 2018-05-12 01:01:48
# Size of source mod 2**32: 914 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='APIKey',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'username', models.CharField(help_text='Wanikani username', max_length=60)),
      (
       'key', models.CharField(help_text='Wanikani v2 api key', max_length=60)),
      (
       'owner', models.ForeignKey(help_text='Django user object', on_delete=(django.db.models.deletion.CASCADE), related_name='+', to=(settings.AUTH_USER_MODEL)))])]