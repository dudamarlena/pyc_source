# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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