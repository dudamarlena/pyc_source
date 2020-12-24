# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cfl/ternaris/marv/pycapnp/buildutils/msg.py
"""logging"""
from __future__ import division
import os, sys, logging
logger = logging.getLogger()
if os.environ.get('DEBUG'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def fatal(msg, code=1):
    logger.error('Fatal: ' + msg)
    exit(code)


def warn(msg):
    logger.error('Warning: ' + msg)


def line(c='*', width=48):
    print c * (width // len(c))