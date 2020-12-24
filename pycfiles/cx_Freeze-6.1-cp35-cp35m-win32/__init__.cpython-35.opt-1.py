# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\__init__.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 431 bytes
import sys
from cx_Freeze.dist import bdist_rpm, build, build_exe, install, install_exe, setup
if sys.platform == 'win32':
    from cx_Freeze.windist import bdist_msi
elif sys.platform == 'darwin':
    from cx_Freeze.macdist import bdist_dmg, bdist_mac
from cx_Freeze.finder import Module, ModuleFinder
from cx_Freeze.freezer import ConfigError, ConstantsModule, Executable, Freezer
__version__ = '6.1'
version = __version__