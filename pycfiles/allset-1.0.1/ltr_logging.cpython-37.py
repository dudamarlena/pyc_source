# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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