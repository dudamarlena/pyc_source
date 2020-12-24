# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/utils/ltr_logging.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 798 bytes
import logging, os, sys

def init_logger(output_dir: str) -> logging.Logger:
    log_format = '[%(levelname)s] %(asctime)s - %(message)s'
    log_dateformat = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=log_format, datefmt=log_dateformat, stream=(sys.stdout), level=(logging.INFO))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(output_dir, 'training.log'))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)