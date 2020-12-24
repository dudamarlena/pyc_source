# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/member/migrations/0008_thirdadherent.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 597 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('accounting', '0012_entrylineaccount_reference_size'),
     ('member', '0007_add_model')]
    operations = [
     migrations.CreateModel(name='ThirdAdherent', fields=[], options={'proxy': True, 
      'default_permissions': [], 
      'indexes': [], 
      'constraints': []}, bases=('accounting.third', ))]