# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/__init__.py
# Compiled at: 2019-05-22 23:43:45
# Size of source mod 2**32: 2444 bytes
from __future__ import absolute_import
from . import version
from _hl.h5type import special_dtype, check_dtype, Reference, RegionReference
from _hl.files import File
from _hl.folders import Folder
from _hl.group import Group, SoftLink, ExternalLink, UserDefinedLink, HardLink
from _hl.dataset import Dataset
from _hl.table import Table
from _hl.datatype import Datatype
from _hl.attrs import AttributeManager
from _hl.serverinfo import getServerInfo
from .config import Config
__version__ = version.version
__doc__ = '\n    This is the h5pyd package, a Python interface to the HDF REST Server.\n\n    Version %s\n \n' % version.version

def enable_ipython_completer():
    import sys
    if 'IPython' in sys.modules:
        ip_running = False
        try:
            from IPython.core.interactiveshell import InteractiveShell
            ip_running = InteractiveShell.initialized()
        except ImportError:
            from IPython import ipapi as _ipapi
            ip_running = _ipapi.get() is not None
        except Exception:
            pass

        if ip_running:
            from . import ipy_completer
            return ipy_completer.load_ipython_extension()
    raise RuntimeError('completer must be enabled in active ipython session')