# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spotify_to_google/log.py
# Compiled at: 2017-07-09 09:04:21
import logging, logging.handlers, os

def setup_logger(name):
    logger = logging.getLogger(name)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)
    fh = logging.handlers.TimedRotatingFileHandler('logs/args.log', when='M', interval=10)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    fh.setLevel(logging.DEBUG)