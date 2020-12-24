# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0016_auto_20190204_1825.py
# Compiled at: 2019-02-10 08:55:09
from __future__ import unicode_literals
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    from django.apps import apps
    Setting = apps.get_model(b'settings', b'Setting')
    FileField = apps.get_model(b'filefields', b'FileField')
    key = b''
    for key_file_type, value_file_type in FileField.FILE_TYPE:
        try:
            value = b''
            if key_file_type == b'P':
                value = b'https://cdn.aparnik.com/static/img/icon_pdf.png'
            elif key_file_type == b'M':
                value = b'https://cdn.aparnik.com/static/img/icon_movie.png'
            elif key_file_type == b'V':
                value = b'https://cdn.aparnik.com/static/img/icon_voice.png'
            elif key_file_type == b'I':
                value = b'https://cdn.aparnik.com/static/img/icon_image.png'
            key = b'FILE_TYPE_%s_ICON' % key_file_type
            Setting.objects.get(key=key)
        except Exception:
            Setting.objects.create(title=b'آیکن مربوط به فایل تایپ %s' % value_file_type, key=key, value=value, value_type=b's', is_show=False, is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0015_auto_20190201_1930')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=migrations.RunPython.noop)]