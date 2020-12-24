# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maciejczyzewski/teax/repository/teax/__init__.py
# Compiled at: 2016-02-02 18:57:49
"""teax package initialization"""
import os
__version__ = '0.0.dev1'
TEAX_WORK_PATH = os.getcwd()
TEAX_REAL_PATH = os.path.dirname(os.path.realpath(__file__))
os.chdir(TEAX_WORK_PATH)
from teax.terminal import TerminalObject
tty = TerminalObject()
from teax.config import ConfigObject
conf = ConfigObject('teax.ini')
import teax.system