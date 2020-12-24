# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/haufe.sharepoint-0.1.9/haufemod/sharepoint/logger.py
# Compiled at: 2014-11-07 17:42:00
import os, sys, logging
handler = logging.StreamHandler(sys.stdout)
frm = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%d.%m.%Y %H:%M:%S')
handler.setFormatter(frm)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
if 'DEBUG_SUDS' in os.environ:
    logger.setLevel(logging.DEBUG)