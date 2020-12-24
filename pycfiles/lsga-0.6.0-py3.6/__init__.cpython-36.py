# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/__init__.py
# Compiled at: 2019-02-10 16:39:57
# Size of source mod 2**32: 490 bytes
import logging, sys
from .engine import GAEngine
from .engine_wrapper import EngineWrapper
__version__ = '0.6.0'
__author__ = 'ShaoZhengjiang <shaozhengjiang@gmail.com>'
logger = logging.getLogger('lsga')
logger.setLevel(logging.INFO)
console_hdlr = logging.StreamHandler(sys.stdout)
console_hdlr.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s   %(levelname)-8s %(message)s')
console_hdlr.setFormatter(formatter)
logger.addHandler(console_hdlr)