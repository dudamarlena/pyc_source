# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/member/migrations/0006_change_ordering.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 835 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('member', '0005_prestation')]
    operations = [
     migrations.AlterModelOptions(name='activity', options={'default_permissions': [], 'ordering': ['name'], 'verbose_name': 'activity', 'verbose_name_plural': 'activities'}),
     migrations.AlterModelOptions(name='subscription', options={'ordering': ['-begin_date'], 'verbose_name': 'subscription', 'verbose_name_plural': 'subscription'}),
     migrations.AlterModelOptions(name='team', options={'default_permissions': [], 'ordering': ['name'], 'verbose_name': 'team', 'verbose_name_plural': 'teams'})]