# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/django_project_templates/templates/newsapps_project/+project+/configs/staging/manage.py
# Compiled at: 2010-03-28 09:05:20
import os, sys
from django.core.management import execute_manager
python_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), '../../../')
apps_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), '../../apps')
sys.path.insert(0, python_path)
sys.path.insert(0, apps_path)
try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == '__main__':
    execute_manager(settings)