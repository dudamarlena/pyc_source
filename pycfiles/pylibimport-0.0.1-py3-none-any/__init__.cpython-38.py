# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\TestLibs\pylibimport\pylibimport\__init__.py
# Compiled at: 2020-05-04 01:10:09
# Size of source mod 2**32: 163 bytes
from .__meta__ import version as __version__
from .utils import make_import_name, get_name_version, is_python_package
from .lib_import import VersionImporter