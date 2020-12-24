# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/settings/migrations/0016_auto_20190204_1825.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1812 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    import django.apps as apps
    Setting = apps.get_model('settings', 'Setting')
    FileField = apps.get_model('filefields', 'FileField')
    key = ''
    for key_file_type, value_file_type in FileField.FILE_TYPE:
        try:
            value = ''
            if key_file_type == 'P':
                value = 'https://cdn.aparnik.com/static/img/icon_pdf.png'
            else:
                if key_file_type == 'M':
                    value = 'https://cdn.aparnik.com/static/img/icon_movie.png'
                else:
                    if key_file_type == 'V':
                        value = 'https://cdn.aparnik.com/static/img/icon_voice.png'
                    else:
                        if key_file_type == 'I':
                            value = 'https://cdn.aparnik.com/static/img/icon_image.png'
                        else:
                            if key_file_type == 'L':
                                value = 'https://cdn.aparnik.com/static/img/icon_image.png'
                            else:
                                continue
            key = 'FILE_TYPE_%s_ICON' % key_file_type
            Setting.objects.get(key=key)
        except Exception:
            Setting.objects.create(title=('آیکن مربوط به فایل تایپ %s' % value_file_type),
              key=key,
              value=value,
              value_type='s',
              is_show=False,
              is_variable_in_home=False)


class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0015_auto_20190201_1930')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=(migrations.RunPython.noop))]