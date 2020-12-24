# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Repos\TestLibs\pylibimport\pylibimport\__init__.py
# Compiled at: 2020-05-04 01:10:09
# Size of source mod 2**32: 163 bytes
from .__meta__ import version as __version__
from .utils import make_import_name, get_name_version, is_python_package
from .lib_import import VersionImporter