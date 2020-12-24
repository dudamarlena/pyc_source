# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0069_auto_20190826_1626.py
# Compiled at: 2019-08-26 04:26:06
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0068_course_template')]
    operations = [
     migrations.AlterField(model_name=b'course', name=b'template', field=models.CharField(blank=True, help_text=b'在项目中custom_user下新建模版文件custom_user_course_section_list_[template].html', max_length=180, null=True, verbose_name=b'模版'))]