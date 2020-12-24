# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0016_auto_20180120_1605.py
# Compiled at: 2018-01-20 03:05:59
from __future__ import unicode_literals
import django.core.files.storage
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0015_auto_20180119_1523')]
    operations = [
     migrations.RemoveField(model_name=b'gradecertfield', name=b'color'),
     migrations.RemoveField(model_name=b'gradecertfield', name=b'width'),
     migrations.AddField(model_name=b'gradecertfield', name=b'font_color', field=models.CharField(default=b'#FFFFFF', max_length=7, verbose_name=b'字体颜色')),
     migrations.AddField(model_name=b'gradecertfield', name=b'font_size', field=models.IntegerField(default=12, max_length=3, verbose_name=b'字体大小')),
     migrations.AddField(model_name=b'gradecertfield', name=b'text_align', field=models.CharField(default=b'left', max_length=180, verbose_name=b'文字对齐'), preserve_default=False),
     migrations.AddField(model_name=b'gradecertfield', name=b'text_bg_color', field=models.CharField(default=b'#FFFFFF', max_length=7, verbose_name=b'文字区域背景颜色')),
     migrations.AddField(model_name=b'gradecertfield', name=b'text_post_x', field=models.IntegerField(default=0, verbose_name=b'文字区域左上角横坐标'), preserve_default=False),
     migrations.AddField(model_name=b'gradecertfield', name=b'text_post_y', field=models.IntegerField(default=0, verbose_name=b'文字区域左上角纵坐标'), preserve_default=False),
     migrations.AddField(model_name=b'gradecertfield', name=b'text_width', field=models.IntegerField(default=100, verbose_name=b'文字区域宽度'), preserve_default=False),
     migrations.AlterField(model_name=b'grade', name=b'cert_image', field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/media/exam/cert', location=b'media/exam/cert'), upload_to=b'', verbose_name=b'证书图片'))]