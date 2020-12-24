# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/files/migrations/0003_auto_20160309_2123.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1076 bytes
import os
from django.db import migrations

def assign_file_type(apps, schema_editor):
    types = {'image':('.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp'), 
     'text':('.txt', '.doc', '.docx'), 
     'spreadsheet':('.csv', '.xls', '.xlsx'), 
     'powerpoint':('.ppt', '.pptx'), 
     'pdf':'.pdf', 
     'video':('.wmv', '.mov', '.mpg', '.mp4', '.m4v'), 
     'zip':'.zip'}
    File = apps.get_model('files', 'File')
    for f in File.objects.all():
        ext = os.path.splitext(f.file.name)[(-1)]
        f_type = ''
        for type in types:
            if ext in types[type]:
                f_type = type
                break

        if f_type:
            File.objects.filter(id=(f.id)).update(f_type=f_type)


class Migration(migrations.Migration):
    dependencies = [
     ('files', '0002_file_f_type')]
    operations = [
     migrations.RunPython(assign_file_type)]