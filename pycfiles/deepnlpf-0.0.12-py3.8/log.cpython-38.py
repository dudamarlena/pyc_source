# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/log.py
# Compiled at: 2020-04-18 14:26:13
# Size of source mod 2**32: 844 bytes
"""[logs]

    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

    https://realpython.com/python-logging/
    https://realpython.com/python-time-module/
    https://github.com/reubano/pygogo
"""
import os, sys, logging, pygogo as gogo
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo('DeepNLPF', low_hdlr=(gogo.handlers.file_hdlr('data.log')),
  low_formatter=formatter,
  high_level='error',
  high_formatter=formatter).logger