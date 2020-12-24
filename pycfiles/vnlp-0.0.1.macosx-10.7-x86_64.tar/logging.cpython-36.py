# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/utils/logging.py
# Compiled at: 2018-06-22 00:48:54
# Size of source mod 2**32: 601 bytes
import logging

def get_logger(name, fout=None, level=logging.INFO, file_level=None):
    """
    Returns a `logging.Logger` object that outputs to stdout and optionally to disk.
    """
    logger = logging.Logger(name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    if fout:
        fh = logging.FileHandler(fout)
        fh.setLevel(file_level or level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger