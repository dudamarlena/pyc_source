# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0009_user_username_validation.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import django.core.validators

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0008_user_unique_together_fields')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'username', field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(regex=b"^[A-Z, a-z, 0-9, ., !, #, $, %, &, ', *, +, -, /, =, ?, ^, _, `]+$", message=b"Field value is not valid. Valid values are: Strings formed with characters from A to Z (uppercase or lowercase), digits from 0 to 9, !, #, $, %, &, ', *, +, -, /, =, ?, ^, _, `")]), preserve_default=True)]