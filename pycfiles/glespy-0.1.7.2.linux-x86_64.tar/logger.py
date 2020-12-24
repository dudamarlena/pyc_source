# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/tools/logger.py
# Compiled at: 2013-09-15 08:13:07
__author__ = 'yarnaid'
import logging
try:
    import colorer
except:
    import glespy.tools.colorer

logging.basicConfig(format='[%(funcName)s][%(asctime)s] %(levelname)s: %(message)s')
logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p')
logging.basicConfig(level=logging.INFO)
logging.basicConfig(levelname=logging.INFO)
logger = logging.getLogger()
logger.INFO = logging.INFO
logger.DEBUG = logging.DEBUG
logger.CRITICAL = logging.CRITICAL
logger.WARNING = logging.WARNING
logger.ERROR = logging.ERROR
logger.NOTSET = logging.NOTSET
logger.setLevel(logger.INFO)
logger.setLevel(logger.DEBUG)