# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/__init__.py
# Compiled at: 2020-05-04 07:05:51
# Size of source mod 2**32: 723 bytes
__version__ = '2.7.0'
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