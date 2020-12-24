# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mydupfilekiller\__init__.py
# Compiled at: 2014-07-06 10:30:46
# Size of source mod 2**32: 303 bytes
__author__ = 'Wiadufa Chen <wiadufachen@gmail.com>'
__version__ = '2.5'
import pyximport
a, b = pyximport.install()
from mydupfilekiller.core import *
from mydupfilekiller.console import *
from mydupfilekiller.gui import *
from mydupfilekiller.exceptions import *
pyximport.uninstall(a, b)