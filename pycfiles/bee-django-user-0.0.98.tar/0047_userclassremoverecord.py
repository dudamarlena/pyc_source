# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0047_userclassremoverecord.py
# Compiled at: 2019-11-15 01:52:10
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_user', '0046_auto_20191114_1630')]
    operations = [
     migrations.CreateModel(name=b'UserClassRemoveRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'created_by', to=settings.AUTH_USER_MODEL, verbose_name=b'操作人')),
      (
       b'new_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'new_class', to=b'bee_django_user.UserClass', verbose_name=b'新班级')),
      (
       b'old_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'old_class', to=b'bee_django_user.UserClass', verbose_name=b'原班级')),
      (
       b'student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'student', to=settings.AUTH_USER_MODEL, verbose_name=b'学生'))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_user_class_remove_record'})]