# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/jobs/migrations/0002_auto_20170910_1701.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1507 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('jobs', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Category',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'name', models.CharField(max_length=255)),
      (
       'slug', models.SlugField()),
      (
       'parent', models.ForeignKey(related_name='children', blank=True, to='jobs.Category', null=True, on_delete=(django.db.models.deletion.CASCADE)))],
       options={'ordering':('name', ), 
      'verbose_name_plural':'Categories'}),
     migrations.AddField(model_name='job',
       name='cat',
       field=models.ForeignKey(related_name='job_cat', on_delete=(django.db.models.deletion.SET_NULL), verbose_name='Category', to='jobs.Category', null=True)),
     migrations.AddField(model_name='job',
       name='sub_cat',
       field=models.ForeignKey(related_name='job_subcat', on_delete=(django.db.models.deletion.SET_NULL), verbose_name='Sub Category', to='jobs.Category', null=True)),
     migrations.AlterUniqueTogether(name='category',
       unique_together=(set([('slug', 'parent')])))]