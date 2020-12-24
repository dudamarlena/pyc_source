# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/utils/logger.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 743 bytes
import logging, os, sys

def setup_logger(name, distributed_rank, save_dir=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if distributed_rank > 0:
        return logger
    stream_handler = logging.StreamHandler(stream=(sys.stdout))
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if save_dir:
        fh = logging.FileHandler(os.path.join(save_dir, 'log.txt'))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger