# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hybrid/skeleton/project/settings.py
# Compiled at: 2016-01-10 07:51:06
from hybrid.wsgi_app import tornadoapp
from hybrid.util import imports
apps = [
 tornadoapp]
controllers = []

def install_controllers():
    for controller in controllers:
        imports(controller)

    from . import controllers as _