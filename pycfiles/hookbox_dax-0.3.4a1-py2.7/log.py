# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/hookbox/log.py
# Compiled at: 2012-07-04 04:55:04
import logging

def setup_logging(config):
    fmt_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=fmt_string)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelName(config.log_level_name))
    formatter = logging.Formatter(fmt_string)
    if config.log_file_err:
        try:
            from logging import handlers
            handler_cls = handlers.WatchedFileHandler
        except:
            handler_cls = logging.FileHandler

        handler = handler_cls(config.log_file_err)
        handler.setFormatter(formatter)
        handler.setLevel(logging.WARN)
        root_logger.addHandler(handler)
    if config.log_file_access:
        try:
            from logging import handlers
            handler_cls = handlers.WatchedFileHandler
        except:
            handler_cls = logging.FileHandler

        handler = handler_cls(config.log_file_access)
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logging.getLogger('access').addHandler(handler)