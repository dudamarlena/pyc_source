# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/toco/__init__.py
# Compiled at: 2019-04-02 13:26:43
# Size of source mod 2**32: 338 bytes
from __future__ import division, print_function, absolute_import, unicode_literals
import logging, os, __main__
logging.basicConfig()
logger = logging.getLogger(__name__)
from .toco import toco
PACKAGEDIR = os.path.dirname(os.path.abspath(__file__))