# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/deploy/modpython.py
# Compiled at: 2009-10-31 23:19:40
import os, sys
from os.path import abspath, dirname, join
from site import addsitedir
VIRTUALENV_BASE = ''
if not VIRTUALENV_BASE:
    raise Exception('VIRTUALENV_BASE is not set correctly.')
activate_this = join(VIRTUALENV_BASE, 'bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
from django.core.handlers.modpython import ModPythonHandler

class PinaxModPythonHandler(ModPythonHandler):

    def __call__(self, req):
        os.environ.update(req.subprocess_env)
        from django.conf import settings
        sys.path.insert(0, abspath(join(dirname(__file__), '../../')))
        sys.path.insert(0, join(settings.PINAX_ROOT, 'apps'))
        sys.path.insert(0, join(settings.PROJECT_ROOT, 'apps'))
        return super(PinaxModPythonHandler, self).__call__(req)


def handler(req):
    return PinaxModPythonHandler()(req)