# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/resumes/migrations/0005_auto_20190816_1502.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1978 bytes
from django.db import migrations

def remove_fb_like_from_custom_templates(apps, schema_editor):
    """
    Remove facebook like buttons from custom templates (the templates pulled down to site).
     
    1) resumes/meta.html
        Remove facebook like block 
    
        {% if show_fb_connect|default:False %}
           <li>{% fb_like_button_iframe resume.get_absolute_url height=20 %}</li>
       {% endif %}
       
    2) resumes/view.html
      Replace
        {% include "resumes/meta.html" with show_fb_connect=True %}
      with
        {% include "resumes/meta.html" %}
    
    """
    import re, os
    from tendenci.apps.theme.utils import get_theme_root
    dir_path = get_theme_root()
    file_path = '{}/templates/resumes/meta.html'.format(dir_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as (f):
            content = f.read()
            p = '{0}([\\d\\D\\s\\S\\w\\W]*?){1}'.format(re.escape('{% if show_fb_connect|default:False %}'), re.escape('{% endif %}'))
            content = re.sub(p, '', content)
        with open(file_path, 'w') as (f):
            f.write(content)
    file_path = '{}/templates/resumes/view.html'.format(dir_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as (f):
            content = f.read()
            p = '{0}'.format(re.escape('{% include "resumes/meta.html" with show_fb_connect=True %}'))
            content = re.sub(p, '{% include "resumes/meta.html" %}', content)
        with open(file_path, 'w') as (f):
            f.write(content)


class Migration(migrations.Migration):
    dependencies = [
     ('resumes', '0004_auto_20190109_1714')]
    operations = [
     migrations.RunPython(remove_fb_like_from_custom_templates)]