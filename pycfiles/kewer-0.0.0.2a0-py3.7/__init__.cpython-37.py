# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/kewer/__init__.py
# Compiled at: 2019-04-25 16:48:20
# Size of source mod 2**32: 306 bytes
from .kewer import Kernel, Drawer
import logging
__version__ = '0.0.0.2a'
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.info(f"kewer v{__version__}")