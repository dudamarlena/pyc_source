# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hybrid/skeleton/project/wsgi.py
# Compiled at: 2016-01-10 06:45:05
from hybrid.middlewares import ChooseAPPMiddleware
from .settings import apps, install_controllers
install_controllers()
application = ChooseAPPMiddleware(*apps)