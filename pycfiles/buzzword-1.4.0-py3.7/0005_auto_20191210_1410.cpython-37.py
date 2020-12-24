# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0005_auto_20191210_1410.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 1132 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0004_auto_20191205_0900')]
    operations = [
     migrations.CreateModel(name='Language',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'name', models.CharField(max_length=255))]),
     migrations.AlterModelOptions(name='corpus',
       options={'verbose_name_plural': 'Corpora'}),
     migrations.AddField(model_name='corpus',
       name='language_link',
       field=models.ForeignKey(null=True,
       on_delete=(django.db.models.deletion.SET_NULL),
       to='explore.Language'))]