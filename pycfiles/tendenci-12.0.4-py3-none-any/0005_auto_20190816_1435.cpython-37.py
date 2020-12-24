# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/jobs/migrations/0005_auto_20190816_1435.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1942 bytes
from django.db import migrations

def remove_fb_like_from_custom_templates(apps, schema_editor):
    """
    Remove facebook like buttons from custom templates (the templates pulled down to site).
     
    1) jobs/meta.html
        Remove facebook like block 
    
        {% if show_fb_connect|default:False %}
           <li>{% fb_like_button_iframe job.get_absolute_url height=20 %}</li>
       {% endif %}
       
    2) jobs/view.html
      Replace
        {% include "jobs/meta.html" with show_fb_connect=True %}
      with
        {% include "jobs/meta.html" %}
    
    """
    import re, os
    from tendenci.apps.theme.utils import get_theme_root
    dir_path = get_theme_root()
    file_path = '{}/templates/jobs/meta.html'.format(dir_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as (f):
            content = f.read()
            p = '{0}([\\d\\D\\s\\S\\w\\W]*?){1}'.format(re.escape('{% if show_fb_connect|default:False %}'), re.escape('{% endif %}'))
            content = re.sub(p, '', content)
        with open(file_path, 'w') as (f):
            f.write(content)
    file_path = '{}/templates/jobs/view.html'.format(dir_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as (f):
            content = f.read()
            p = '{0}'.format(re.escape('{% include "jobs/meta.html" with show_fb_connect=True %}'))
            content = re.sub(p, '{% include "jobs/meta.html" %}', content)
        with open(file_path, 'w') as (f):
            f.write(content)


class Migration(migrations.Migration):
    dependencies = [
     ('jobs', '0004_auto_20180315_0857')]
    operations = [
     migrations.RunPython(remove_fb_like_from_custom_templates)]