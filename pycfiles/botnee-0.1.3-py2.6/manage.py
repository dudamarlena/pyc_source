# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/web/manage.py
# Compiled at: 2012-04-17 08:42:52
from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings')
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings
from setproctitle import setproctitle
setproctitle('botnee-web')
if __name__ == '__main__':
    execute_manager(settings)