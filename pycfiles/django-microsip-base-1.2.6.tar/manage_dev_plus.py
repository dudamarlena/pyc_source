# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\django-microsip-base\django_microsip_base\manage_dev_plus.py
# Compiled at: 2019-09-09 14:23:54
import os, sys

def add_debug_apps():
    """
        Para que se pueda estar depurando una aplicacion
        sin instalar la aplicacion realmente app como microsip_api.
    """
    REPOSITORIES_PATH = str(os.path.abspath(__file__ + '/../../../'))
    new_path = ('{}\\{}').format(REPOSITORIES_PATH, 'django-microsip-api')
    print new_path
    sys.path.append(new_path)
    DJMICROSIP_APPS = str(os.path.join(REPOSITORIES_PATH, 'djmicrosip_apps'))
    debug_apps = []
    debug_apps = os.listdir(DJMICROSIP_APPS)
    for debug_app in debug_apps:
        new_path = ('{}\\{}').format(DJMICROSIP_APPS, debug_app)
        sys.path.append(new_path)


add_debug_apps()
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_microsip_base.settings.dev_plus')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)