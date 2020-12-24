# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\source\Tools\LogError.py
# Compiled at: 2019-02-21 18:44:24
# Size of source mod 2**32: 775 bytes
import logging, sys
from Tools.BasePara import error_log_path
handler = logging.FileHandler(error_log_path)
handler.setLevel(logging.WARNING)
logging.basicConfig(level=(logging.WARNING), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)