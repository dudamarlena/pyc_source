# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_srv/logger.py
# Compiled at: 2020-04-13 12:15:39
# Size of source mod 2**32: 661 bytes
"""
oathldap_srv.logger - initialite custom logger
"""
import logging

def init_logger(cfg):
    """
    Create logger instance from config data
    """
    if cfg.logging_conf is not None:
        from logging.config import fileConfig
        logging.config.fileConfig(cfg.logging_conf)
    else:
        logging.basicConfig(level=(cfg.log_level),
          format='%(asctime)s %(name)s %(levelname)s: %(message)s',
          datefmt='%Y-%m-%d %H:%M:%S')
    _logger = logging.getLogger(cfg.logger_name)
    _logger.name = cfg.default_section
    return _logger