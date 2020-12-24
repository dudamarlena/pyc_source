# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/member/migrations/0005_prestation.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 1648 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('invoice', '0012_print_article'),
     ('member', '0004_subscription_status')]
    operations = [
     migrations.CreateModel(name='Prestation', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=50, verbose_name='name')),
      (
       'description', models.TextField(default='', null=True, verbose_name='description')),
      (
       'activity', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='member.Activity', verbose_name='activity')),
      (
       'article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Article', verbose_name='article')),
      (
       'team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='member.Team', verbose_name='team'))], options={'default_permissions': [], 
      'ordering': ['team__name', 'activity__name'], 
      'verbose_name': 'prestation', 
      'verbose_name_plural': 'prestations'}),
     migrations.AddField(model_name='subscription', name='prestations', field=models.ManyToManyField(blank=True, to='member.Prestation', verbose_name='prestations'))]