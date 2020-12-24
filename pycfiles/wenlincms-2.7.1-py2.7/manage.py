# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/project_template/manage.py
# Compiled at: 2016-05-20 23:42:06
from __future__ import absolute_import, unicode_literals
import os, sys
from mainsys.settings import PROJECT_ROOT, PROJECT_DIRNAME
sys.path.append(os.path.abspath(os.path.join(PROJECT_ROOT, b'..')))
for i, arg in enumerate(sys.argv):
    if arg.startswith(b'--site'):
        os.environ[b'wenlincms_SITE_ID'] = arg.split(b'=')[1]
        sys.argv.pop(i)

if __name__ == b'__main__':
    settings_module = b'%s.settings' % PROJECT_DIRNAME
    os.environ.setdefault(b'DJANGO_SETTINGS_MODULE', settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)