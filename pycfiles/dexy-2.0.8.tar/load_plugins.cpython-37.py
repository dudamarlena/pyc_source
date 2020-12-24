# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/load_plugins.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 454 bytes
import dexy.filters, dexy.reporters, dexy.parsers, dexy.datas, pkg_resources
for dist in pkg_resources.working_set:
    if dist.key.startswith('dexy-'):
        import_pkg = dist.egg_name().split('-')[0]
        try:
            __import__(import_pkg)
        except ImportError as e:
            try:
                print(('plugin', import_pkg, 'not registered because', e))
            finally:
                e = None
                del e