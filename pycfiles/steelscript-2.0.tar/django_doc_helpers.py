# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript/docs/_ext/django_doc_helpers.py
# Compiled at: 2015-09-25 13:31:42
import os, sys, inspect
THIS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.join(THIS_DIR, '..', 'appfwk_project')
if not os.path.exists(PROJECT_DIR):
    os.system('steel appfwk mkproject -d %s' % PROJECT_DIR)
    os.system('cd %s ; steel appfwk init' % PROJECT_DIR)
    os.system('touch %s/__init__.py' % PROJECT_DIR)
sys.path.append(PROJECT_DIR)
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_settings')
django.setup()
from django.db import models
from django.utils.html import strip_tags
from django.utils.encoding import force_unicode
from steelscript.appfwk.apps.datasource.models import DatasourceTable

def process_docstring(app, what, name, obj, options, lines):
    from django.db import models
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        fields = obj._meta._fields()
        for field in fields:
            help_text = strip_tags(force_unicode(field.help_text))
            verbose_name = force_unicode(field.verbose_name).capitalize()
            if help_text:
                lines.append(':param %s: %s' % (field.attname, help_text))
            else:
                lines.append(':param %s: %s' % (field.attname, verbose_name))
            lines.append(':type %s: %s' % (field.attname, type(field).__name__))

    elif inspect.ismethod(obj) and name.endswith('create') and obj.__doc__ is None and DatasourceTable in obj.im_self.__bases__:
        for line in inspect.getdoc(obj.im_self).split('\n'):
            lines.append(line)

    return lines