# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0011_auto_20180118_1719.py
# Compiled at: 2018-01-18 04:19:13
from __future__ import unicode_literals
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0010_auto_20180118_1534')]
    operations = [
     migrations.CreateModel(name=b'GradeCertField', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180)),
      (
       b'field', models.CharField(max_length=180)),
      (
       b'width', models.IntegerField()),
      (
       b'color', models.CharField(max_length=7))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_exam_grade_cert_field'}),
     migrations.AlterField(model_name=b'grade', name=b'cert_image', field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'media/exam/cert'), upload_to=b'', verbose_name=b'证书图片')),
     migrations.AddField(model_name=b'gradecertfield', name=b'grade', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_exam.Grade'))]