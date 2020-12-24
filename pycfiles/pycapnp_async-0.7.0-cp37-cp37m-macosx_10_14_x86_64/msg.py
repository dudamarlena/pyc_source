# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cfl/ternaris/marv/pycapnp/buildutils/msg.py
__doc__ = 'logging'
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