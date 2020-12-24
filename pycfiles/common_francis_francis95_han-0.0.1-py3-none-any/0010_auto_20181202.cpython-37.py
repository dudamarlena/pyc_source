# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0010_auto_20181202.py
# Compiled at: 2019-06-21 06:40:20
# Size of source mod 2**32: 2593 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('common', '0009_auto_20181010')]
    operations = [
     migrations.AlterModelOptions(name='history',
       options={'verbose_name':'historique', 
      'verbose_name_plural':'historiques'}),
     migrations.AlterModelOptions(name='historyfield',
       options={'verbose_name':'historique de champ modifié', 
      'verbose_name_plural':'historiques de champs modifiés'}),
     migrations.AddField(model_name='historyfield',
       name='editable',
       field=models.BooleanField(default=True, editable=False, verbose_name='éditable')),
     migrations.AlterField(model_name='global',
       name='content_type',
       field=models.ForeignKey(editable=False, on_delete=(django.db.models.deletion.CASCADE), related_name='+', to='contenttypes.ContentType', verbose_name="type d'entité")),
     migrations.AlterField(model_name='history',
       name='content_type',
       field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='+', to='contenttypes.ContentType', verbose_name="type d'entité")),
     migrations.AlterField(model_name='history',
       name='user',
       field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='histories', to=(settings.AUTH_USER_MODEL), verbose_name='utilisateur')),
     migrations.AlterField(model_name='historyfield',
       name='history',
       field=models.ForeignKey(editable=False, on_delete=(django.db.models.deletion.CASCADE), related_name='fields', to='common.History', verbose_name='historique')),
     migrations.AlterField(model_name='metadata',
       name='content_type',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='+', to='contenttypes.ContentType', verbose_name="type d'entité")),
     migrations.AlterField(model_name='serviceusage',
       name='user',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='usages', to=(settings.AUTH_USER_MODEL), verbose_name='utilisateur'))]