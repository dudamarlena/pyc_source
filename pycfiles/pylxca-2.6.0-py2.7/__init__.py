# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/__init__.py
# Compiled at: 2019-12-06 06:32:09
__version__ = '2.6.0'
from pylxca.pylxca_api import *
from pylxca.pylxca_cmd import *
from pylxca.pylxca_cmd.lxca_pyshell import *
import logging
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
import logging.config
pylxca.pylxca_api.lxca_rest().set_log_config()
pyshell()