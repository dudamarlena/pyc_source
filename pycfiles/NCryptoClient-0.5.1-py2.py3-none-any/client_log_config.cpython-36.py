# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\PyCharm Projects\Python-2-Lesson2-Homework-KrylovAM\Solution\ClientApp\Log\client_log_config.py
# Compiled at: 2018-03-18 16:45:22
# Size of source mod 2**32: 962 bytes
"""
Экземляр логгера для клиентской части хранится в данном модуле.
"""
import os, logging
from Solution.Shared.Logger.log_config import Logger
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'client.log')
client_logger = Logger('client', CLIENT_LOG_FILE_PATH, '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s', 'd', logging.INFO, logging.INFO)