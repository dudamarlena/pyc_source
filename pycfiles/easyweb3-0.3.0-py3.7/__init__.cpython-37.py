# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/easyweb3/__init__.py
# Compiled at: 2020-01-18 08:11:43
# Size of source mod 2**32: 302 bytes
from .easyweb3 import EasyWeb3
import logging
__version__ = '0.3.0'
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.info(f"EasyWeb3 v{__version__}")