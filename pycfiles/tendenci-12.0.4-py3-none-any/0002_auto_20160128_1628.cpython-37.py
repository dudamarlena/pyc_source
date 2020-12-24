# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/projects/migrations/0002_auto_20160128_1628.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1848 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0001_initial'),
     ('projects', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Category',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'name', models.CharField(max_length=300, verbose_name='name')),
      (
       'position', models.IntegerField(default=0, blank=True))],
       options={'ordering': ('position', )}),
     migrations.CreateModel(name='CategoryPhoto',
       fields=[
      (
       'file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, on_delete=(django.db.models.deletion.CASCADE), to='files.File'))],
       options={'abstract': False},
       bases=('files.file', )),
     migrations.AlterField(model_name='project',
       name='project_number',
       field=models.OneToOneField(null=True, blank=True, on_delete=(django.db.models.deletion.CASCADE), to='projects.ProjectNumber')),
     migrations.AddField(model_name='category',
       name='image',
       field=models.ForeignKey(default=None, to='projects.CategoryPhoto', help_text='Photo that represents this category.', null=True, on_delete=(django.db.models.deletion.CASCADE))),
     migrations.AddField(model_name='project',
       name='category',
       field=models.ManyToManyField(to='projects.Category', blank=True))]