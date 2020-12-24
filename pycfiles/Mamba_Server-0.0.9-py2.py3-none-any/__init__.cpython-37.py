# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/__init__.py
# Compiled at: 2020-05-09 09:17:44
# Size of source mod 2**32: 469 bytes
"""
Mamba - a framework for controlling ground equipment
"""
import sys
__all__ = [
 '__version__', 'version_info']
import pkgutil
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
version_info = tuple(((int(v) if v.isdigit() else v) for v in __version__.split('.')))
del pkgutil
if sys.version_info < (3, 5):
    print('Mamba %s requires Python 3.5' % __version__)
    sys.exit(1)