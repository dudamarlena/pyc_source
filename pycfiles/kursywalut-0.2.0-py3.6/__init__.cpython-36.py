# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kursywalut/__init__.py
# Compiled at: 2018-12-20 11:59:26
# Size of source mod 2**32: 784 bytes
"""Top-level package for KursyWalut."""
import logging
from .version import __version__
from . import funcs, handlers, parsers, interface
__author__ = 'Bart Grzybicki'
__email__ = 'bgrzybicki@gmail.com'
__all__ = '__version__'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
handler = logging.FileHandler('kursywalut.log')
handler.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)