# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/projects/migrations/0003_auto_20180928_1713.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1401 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('projects', '0002_auto_20160128_1628')]
    operations = [
     migrations.AlterModelOptions(name='documents',
       options={'verbose_name':'Document', 
      'verbose_name_plural':'Documents'}),
     migrations.AlterModelOptions(name='teammembers',
       options={'verbose_name':'Team Member', 
      'verbose_name_plural':'Team Members'}),
     migrations.RenameField(model_name='documents',
       old_name='type',
       new_name='doc_type'),
     migrations.RenameField(model_name='documenttype',
       old_name='type',
       new_name='type_name'),
     migrations.AlterField(model_name='project',
       name='client',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='projects.ClientList')),
     migrations.AlterField(model_name='project',
       name='project_manager',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='projects.ProjectManager'))]