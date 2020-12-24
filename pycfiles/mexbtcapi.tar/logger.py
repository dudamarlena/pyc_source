# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/goncalopp/private/mydocs/programacao/python/mexbtcapi/mexbtcapi/logger.py
# Compiled at: 2012-09-28 22:46:36
import sys, logging
log = logging.getLogger('mexbtcapi')
formatter = logging.Formatter('MEXBTCAPI: %(message)s')
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.INFO)