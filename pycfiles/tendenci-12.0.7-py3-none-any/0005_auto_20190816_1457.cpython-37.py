# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/pages/migrations/0005_auto_20190816_1457.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1339 bytes
from django.db import migrations

def remove_fb_like_from_custom_templates(apps, schema_editor):
    """
    Remove facebook like buttons from custom templates (the templates pulled down to site).
     
    1) pages/meta.html
        Remove facebook like block 
    
        {% if show_fb_connect|default:False %}
           {% fb_like_button_iframe news.get_absolute_url height=20 %}
       {% endif %}
       
    
    """
    import re, os
    from tendenci.apps.theme.utils import get_theme_root
    dir_path = get_theme_root()
    file_path = '{}/templates/pages/meta.html'.format(dir_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as (f):
            content = f.read()
            p = '{0}([\\d\\D\\s\\S\\w\\W]*?){1}'.format(re.escape('{% if show_fb_connect|default:False %}'), re.escape('{% endif %}'))
            content = re.sub(p, '', content)
        with open(file_path, 'w') as (f):
            f.write(content)


class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0004_auto_20190815_1719')]
    operations = [
     migrations.RunPython(remove_fb_like_from_custom_templates)]