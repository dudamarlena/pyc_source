# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0020_auto_20190515_1427.py
# Compiled at: 2019-05-15 02:27:43
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0019_auto_20190513_1315')]
    operations = [
     migrations.RemoveField(model_name=b'userquestion', name=b'answer_option_id'),
     migrations.AddField(model_name=b'userquestion', name=b'answer_option', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Option'))]