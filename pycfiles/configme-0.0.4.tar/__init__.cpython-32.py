# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/configmaster/__init__.py
# Compiled at: 2015-08-26 07:54:26
from . import JSONConfigFile, INIConfigFile, SPyCfg
from .exc import FiletypeNotSupportedException
try:
    from . import YAMLConfigFile
except FiletypeNotSupportedException:
    YAMLConfigFile = lambda x: ImportError('You have not installed the PyYAML library. Install it via `pip install PyYAML`.')