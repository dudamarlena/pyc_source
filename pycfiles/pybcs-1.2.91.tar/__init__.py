# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\yanglin\test/..\pybcs\__init__.py
# Compiled at: 2012-03-18 20:38:22
import logging
from bcs import BCS
from bucket import Bucket
__all__ = [
 'bcs', 'bucket', 'object']
from common import NotImplementException
from common import system
from common import md5_for_file
from httpc import *
from httpc import logger

def init_logging(set_level=logging.INFO, console=True, log_file_path=None):
    common.init_logging(httpc.logger, set_level, console, log_file_path)