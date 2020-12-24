# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/circleci/.pyenv/versions/3.6.5/lib/python3.6/machinery.py
# Compiled at: 2019-03-22 00:31:38
# Size of source mod 2**32: 844 bytes
import _imp
from ._bootstrap import ModuleSpec
from ._bootstrap import BuiltinImporter
from ._bootstrap import FrozenImporter
from ._bootstrap_external import SOURCE_SUFFIXES, DEBUG_BYTECODE_SUFFIXES, OPTIMIZED_BYTECODE_SUFFIXES, BYTECODE_SUFFIXES, EXTENSION_SUFFIXES
from ._bootstrap_external import WindowsRegistryFinder
from ._bootstrap_external import PathFinder
from ._bootstrap_external import FileFinder
from ._bootstrap_external import SourceFileLoader
from ._bootstrap_external import SourcelessFileLoader
from ._bootstrap_external import ExtensionFileLoader

def all_suffixes():
    return SOURCE_SUFFIXES + BYTECODE_SUFFIXES + EXTENSION_SUFFIXES