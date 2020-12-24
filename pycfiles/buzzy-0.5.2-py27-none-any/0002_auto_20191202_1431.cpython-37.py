# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0002_auto_20191202_1431.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 1274 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0001_initial')]
    operations = [
     migrations.RenameField(model_name='corpus',
       old_name='diabled',
       new_name='disabled'),
     migrations.AddField(model_name='corpus',
       name='add_governor',
       field=models.BooleanField(null=True)),
     migrations.AddField(model_name='corpus',
       name='name',
       field=models.CharField(default='name', max_length=255),
       preserve_default=False),
     migrations.AlterField(model_name='corpus',
       name='date',
       field=models.DateField(null=True)),
     migrations.AlterField(model_name='corpus',
       name='len',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='corpus',
       name='slug',
       field=models.SlugField(max_length=255, unique=True)),
     migrations.AlterField(model_name='corpus',
       name='url',
       field=models.URLField(max_length=255, null=True))]