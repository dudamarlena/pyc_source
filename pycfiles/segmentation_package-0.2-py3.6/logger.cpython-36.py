# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\segmentation_module\segmentation_api\logger.py
# Compiled at: 2019-03-11 07:36:48
# Size of source mod 2**32: 1326 bytes
import logging, os
from shutil import copyfile

class Logger(object):

    def __init__(self, path, mode='INFO'):
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        else:
            self.path = path
            self.clear_log()
            logger = logging.getLogger(__name__)
            if mode == 'DEBUG':
                log_type = logging.DEBUG
            else:
                log_type = logging.INFO
        logger.setLevel(log_type)
        if logger.handlers:
            logger.handlers = []
        handler = logging.FileHandler(self.path)
        handler.setLevel(log_type)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    def clear_log(self):
        with open(self.path, 'w'):
            pass

    def log_message(self, message, mode='info'):
        if mode == 'info':
            self.logger.info(message)
        elif mode == 'debug':
            self.logger.info(message)

    def move_file(self, new_path):
        log_filename = os.path.basename(self.path)
        copyfile(self.path, os.path.join(new_path, log_filename))
        self.clear_log()