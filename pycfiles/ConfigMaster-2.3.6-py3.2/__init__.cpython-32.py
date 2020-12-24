# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/configmaster/__init__.py
# Compiled at: 2015-08-26 07:54:26
from . import JSONConfigFile, INIConfigFile, SPyCfg
from .exc import FiletypeNotSupportedException
try:
    from . import YAMLConfigFile
except FiletypeNotSupportedException:
    YAMLConfigFile = lambda x: ImportError('You have not installed the PyYAML library. Install it via `pip install PyYAML`.')