# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/2017-A/Dropbox/python_libraries/Pywire/pywire/__init__.py
# Compiled at: 2018-02-10 01:33:51
import sys
if sys.version_info[0] != 2:
    raise Exception('Pywire only works with Python 2.7')
from .main import Signal, generate_vhdl, generate_ucf
from .bram import BRAM
from .component import Component, FromText
from .build import build