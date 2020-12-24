# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0080_auto_20191227_1525.py
# Compiled at: 2019-12-27 02:25:15
from __future__ import unicode_literals
import bee_django_object_field.custom_fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course', '0079_section_pass_cooldown')]
    operations = [
     migrations.CreateModel(name=b'UserCertifyRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'status', models.IntegerField(choices=[(0, '未提交'), (1, '已提交'), (2, '通过'), (3, '驳回'), (4, '关闭')], default=0, verbose_name=b'状态')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'operated_at', models.DateTimeField(blank=True, null=True, verbose_name=b'操作时间')),
      (
       b'detail', bee_django_object_field.custom_fields.DictField(blank=True, null=True, verbose_name=b'添加时的详细数据')),
      (
       b'operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'操作者')),
      (
       b'user_course_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserCourseSection'))], options={b'ordering': [
                    b'-id'], 
        b'db_table': b'bee_django_course_user_certify_record'}),
     migrations.AddField(model_name=b'section', name=b'need_certify', field=models.BooleanField(default=False, verbose_name=b'是否需要认证'))]