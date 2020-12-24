# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mappyfile\__init__.py
# Compiled at: 2020-01-11 08:01:06
import logging, pkg_resources, sys
from types import ModuleType
from mappyfile.utils import open, load, loads, find, findall, findunique, dumps, dump, save
from mappyfile.utils import findkey, update, validate
__version__ = '0.8.4'
__all__ = [
 'open', 'load', 'loads', 'find', 'findall', 'findunique', 'dumps', 'dump', 'save',
 'findkey', 'update', 'validate']
plugins = ModuleType('mappyfile.plugins')
sys.modules['mappyfile.plugins'] = plugins
for ep in pkg_resources.iter_entry_points(group='mappyfile.plugins'):
    setattr(plugins, ep.name, ep.load())

try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


logging.getLogger('mappyfile').addHandler(NullHandler())