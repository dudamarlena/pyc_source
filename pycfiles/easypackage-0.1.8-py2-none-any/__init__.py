# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grimen/Dev/Private/python-easypackage/easypackage/__init__.py
# Compiled at: 2018-06-21 23:22:19
import sys
from os import path
CURRENT_PATH = path.abspath(path.dirname(__file__))
ROOT_PATH = path.abspath(path.join(CURRENT_PATH, '..'))
try:
    sys.path.index(ROOT_PATH)
except ValueError:
    sys.path.append(ROOT_PATH)

import easypackage.__errors__ as __errors__