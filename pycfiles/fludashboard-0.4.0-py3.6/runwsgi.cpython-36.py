# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fludashboard/runwsgi.py
# Compiled at: 2018-02-01 19:31:43
# Size of source mod 2**32: 792 bytes
from . import settings
import os, sys

def startup():
    try:
        import gunicorn
    except:
        raise Exception('[EE] GUNICORN NOT FOUND.')

    path_root = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(path_root, 'runwsgi.sh')
    for setting_variable in dir(settings):
        if setting_variable.startswith('__'):
            pass
        else:
            v = settings.__dict__[setting_variable]
            if isinstance(v, str):
                os.environ[setting_variable] = v

    os.environ['PYTHONPATH'] = os.path.dirname(sys.executable)
    os.environ['PATH'] += ':' + os.environ['PYTHONPATH']
    os.system('python --version')
    os.system('/bin/bash %s' % path_file)


if __name__ == '__main__':
    startup()