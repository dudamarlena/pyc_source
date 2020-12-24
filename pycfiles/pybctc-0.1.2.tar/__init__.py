# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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