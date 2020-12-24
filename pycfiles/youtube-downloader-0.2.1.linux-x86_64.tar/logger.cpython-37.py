# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blooser/anaconda3/lib/python3.7/site-packages/youtubedownloader/logger.py
# Compiled at: 2020-04-25 08:40:29
# Size of source mod 2**32: 296 bytes
import logging
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s: %(message)s'))

def create_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger