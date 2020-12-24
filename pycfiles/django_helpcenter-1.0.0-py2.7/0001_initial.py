# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0001_initial.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Article', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(db_index=True, help_text=b'An article title is restricted to 200 characters.', max_length=200, verbose_name=b'Article')),
      (
       b'body', models.TextField(help_text=b'The body of an article can contain HTML as well as text.', verbose_name=b'Article Body Content')),
      (
       b'time_published', models.DateTimeField(default=django.utils.timezone.now, help_text=('Please use the following format: ',
                                                                   '<em>YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]</em>'), verbose_name=b'Time Published'))])]