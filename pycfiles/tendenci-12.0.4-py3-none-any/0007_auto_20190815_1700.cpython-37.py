# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/articles/migrations/0007_auto_20190815_1700.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 1608 bytes
from django.db import migrations

def remove_google_profile_from_article_view(apps, schema_editor):
    """
    Remove the google_profile block from article/view.html
    
        {% if article.google_profile %}
            {% if article.has_google_author %}
                <a href="{{ article.google_profile }}?rel=author">{% trans "View Author's Google+ Profile" %}</a>
            {% elif article.has_google_publisher %}
                <a href="{{ article.google_profile }}" rel="publisher">{% trans "View Publisher's Google+ Page" %}</a>
            {% endif %}
        {% endif %}
    
    """
    import re, os
    from tendenci.apps.theme.utils import get_theme_root
    dir_path = get_theme_root()
    file_path = '{}/templates/articles/view.html'.format(dir_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as (f):
            content = f.read()
            p = '{0}([\\d\\D\\s\\S\\w\\W]*?){1}([\\s\\S]*?){2}'.format(re.escape('{% if article.google_profile %}'), re.escape('{% endif %}'), re.escape('{% endif %}'))
            content = re.sub(p, '', content)
        with open(file_path, 'w') as (f):
            f.write(content)


class Migration(migrations.Migration):
    dependencies = [
     ('articles', '0006_remove_article_google_profile')]
    operations = [
     migrations.RunPython(remove_google_profile_from_article_view)]