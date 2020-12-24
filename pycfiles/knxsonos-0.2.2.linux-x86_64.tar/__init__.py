# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/knxsonos/__init__.py
# Compiled at: 2016-04-09 16:52:51
import logging, logging.handlers, sys
if '-d' in sys.argv:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('knxsonos')
logger.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
fh = logging.handlers.RotatingFileHandler('/tmp/knxsonos.log', maxBytes=1048576, backupCount=5)
fh.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)