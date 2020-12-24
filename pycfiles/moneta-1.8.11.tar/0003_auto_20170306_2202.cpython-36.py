# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/migrations/0003_auto_20170306_2202.py
# Compiled at: 2017-07-28 01:43:32
# Size of source mod 2**32: 518 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('repository', '0002_auto_20161226_2320')]
    operations = [
     migrations.AlterField(model_name='elementsignature',
       name='method',
       field=models.CharField(choices=[('gpg', 'GnuPG'), ('x509', 'x509 (openSSL/libreSSL)')], db_index=True, max_length=10, verbose_name='méthode de signature'))]