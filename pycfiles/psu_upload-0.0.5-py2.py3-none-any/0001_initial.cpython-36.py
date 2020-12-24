# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mjg/git/django/psu/psu-infotext/psu_infotext/migrations/0001_initial.py
# Compiled at: 2019-07-29 18:37:11
# Size of source mod 2**32: 1050 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Infotext',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'app_code', models.CharField(help_text='Application that this text belongs to', max_length=15, verbose_name='Application Code')),
      (
       'text_code', models.CharField(help_text='Unique identifier for this text instance', max_length=80, verbose_name='Text Identifier')),
      (
       'user_edited', models.CharField(choices=[('N', 'No'), ('Y', 'Yes')], default='N', help_text='Has this text been modified from its coded value?', max_length=1)),
      (
       'content', models.TextField(verbose_name='Text Content')),
      (
       'last_updated', models.DateTimeField(auto_now=True))])]