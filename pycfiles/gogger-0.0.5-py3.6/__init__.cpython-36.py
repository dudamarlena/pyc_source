# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gogger/__init__.py
# Compiled at: 2018-11-28 02:16:45
# Size of source mod 2**32: 1078 bytes
import datetime, logging, os
from logging import handlers
from gogger.level_filter import LevelFilter

class Gogger(object):

    def __init__(self, max_level=40, log_path='log'):
        self.max_level = max_level
        self.log_path = log_path
        if not os.path.exists(log_path):
            os.mkdir(log_path)

    def get_logger(self, spider_name, logger_name=None):
        logger = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        for i in range(self.max_level, 0, -10):
            file_name = '{log_dir}/{spider_name}_{pid}_{time}_{level}.log'.format(log_dir=(self.log_path),
              spider_name=spider_name,
              pid=(os.getpid()),
              time=(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')),
              level=(logging.getLevelName(i)))
            max_bytes = 1048576 * i * i
            _handler = handlers.RotatingFileHandler(filename=file_name, maxBytes=max_bytes)
            _handler.setLevel(i)
            _handler.addFilter(LevelFilter(level=i))
            _handler.setFormatter(formatter)
            logger.addHandler(_handler)

        return logger