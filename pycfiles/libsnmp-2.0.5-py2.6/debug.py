# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/debug.py
# Compiled at: 2008-10-18 18:59:45
import logging, os

class snmpLogger(logging.Logger):

    def __init__(self, name):
        pid = os.getpid()
        FORMAT = '%(asctime)s [' + str(pid) + '] %(name)s: %(levelname)s - %(message)s'
        level = logging.DEBUG
        logging.Logger.__init__(self, name, level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(FORMAT)
        handler.setFormatter(formatter)
        self.addHandler(handler)


logging.setLoggerClass(snmpLogger)