# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0023_auto_20190524_1705.py
# Compiled at: 2019-05-24 05:05:10
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0022_part_image')]
    operations = [
     migrations.CreateModel(name=b'QuestionPrize', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'correct_count', models.IntegerField(unique=True, verbose_name=b'答对问题的数量')),
      (
       b'coin', models.IntegerField(verbose_name=b'奖励M币'))], options={b'ordering': [
                    b'correct_count'], 
        b'db_table': b'bee_django_course_simple_question_prize'}),
     migrations.AddField(model_name=b'userpart', name=b'prize_coin', field=models.IntegerField(default=0, verbose_name=b'奖励的m币'))]